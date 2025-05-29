# Quick investigation

In this part we are going to crawl through the app and discover ways to clean it up and layer things according to clean(er) architecture. We will handle decoupling part later on and related questions once we have necessary background introduction.

## Layering data operations

Let’s start with investigating how well our business logic is defined and clean of cross-layer contamination, as it is main concern of our clean architecture refactoring exercise.

Lets work on a concrete example, this is how we list items in a cart:

```python
def list_items_in_cart(user_id, db):
    cart_items = find_cart_items_for_user_id(user_id, db)
    return AddToCartResponse(items=list(map(cart_item_model_to_schema, cart_items)))
```

As we can immediately spot, we rely on db in our business logic, creating dependency on interface in use case, but that is not the only interface we are hardcoding here, as we are preparing response data and handle http exceptions in our use case. This is also not the job of our business logic.

What we should have here is:
- Clean scenarios of use cases that got injected with external dependencies that are behind a an interface for DI.
- All web related details need to sit on framework part

After refactoring we should see here something like:

```python
async def get_cart_items(cart_repository: CartRepository, user_id: UUID) -> List[CartItem]:
    """Get all items in a user's cart."""
    cart = await cart_repository.get_by_user_id(user_id)
    if not cart:
        return []
    return cart.items
```

Where Items are defined domain objects. We are using asynchronous code here ad it makes sense to rewrite repositories in an asynchronous fashion to enable better performance and patterns like data loader.

In API layer we can have sth like this:

```python
@user_router.get("/cart/{user_id}", response_model=AddToCartResponse)
async def list_items_in_cart(
    user_id: UUID,
    cart_repository: PostgresCartRepository = Depends(get_cart_repository),
) -> AddToCartResponse:
    """List all items in a user's cart."""
    cart_items = await get_cart_items(cart_repository, user_id)
    return AddToCartResponse(
        items=[
            CartItemResponse(
                item_id=item.item_id,
                quantity=item.quantity,
            )
            for item in cart_items
        ]
    )
```

This way we can get instance of repo that we are interested in interface layer, get business relevant objects from use case and handle all web glue code in the API.

Also, right now we can test our business logic as we want in an isolation, everything is passed as an input argument and tests shouldn’t care about the db or web either.

Ok, let’s go deeper into the onion as we are still missing the repo part. We already used interface for that in our use case and concrete instance in our API. We need to create an ABC for repo base and create concrete implementation for postgres, which will sit in infrastructure or interfaces or db or whatever we want to call that part of app structure.

Example method:
```python
class CartRepository(ABC):
    """Interface for cart persistence operations."""

    (…)

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get a user's cart (for viewing and modifying cart contents)."""
        pass

    …
```

Lets go to implementation of that:
```python
class PostgresCartRepository(CartRepository):
    """PostgreSQL implementation of the cart repository."""

    (…)

    async def get_by_user_id(self, user_id: UUID) -> Optional[Cart]:
        """Get a user's cart by their user ID."""
        stmt = select(CartModel).where(CartModel.user_id == user_id)
        result = await self.session.execute(stmt)
        cart_model = result.scalar_one_or_none()

        if not cart_model:
            return None

        return self._to_domain(cart_model)
```

Will not cover more for brevity, obviously there is a lot of potentially important logic related to errors, data inconsistency, rollbacks, data validation, etc. that is too much to get into in a short refactoring session. _to_domain method handles translation between DB data and entity so we do not spill any details out.

## Data model issues

At this point it’s probably good moment to focus a little bit on a data model, and here are some potential issues.

### Keys everywhere

Using foreign key to User.id in Cart as a PK is probably a bad idea as we are limiting ourselves to a single cart per user and deeply interconnected with user model. I would have separate UUID for cart as PK and maybe for now have unique constant on id+active flag. There are different ways to handle order creation and flow, but keeping cart in a ORDERED state or sth like this would be better for keeping track of data flow and troubleshooting, also enables new user scenarios if we want to come back to cart stage for any reason. Right now it would be impossible, even with admin intervention.

What is even more troubling is hard connection between item and cart item, as it both FK and PK. This is a clear red flag crossing domain boundary and as long as it persists separating those services is virtually impossible. We would need to keep synced db table with items on user service to satisfy those constraints. This is a clear high priority candidate for refactoring to get rid of and just use UUID and persisting objects.
### Consistency and transparency 

What happens when an item is removed from the store? How do we handle relations to carts? Don’t we want to see the cart that led to order creation so we can do admin interventions and debug? Maybe we want them for metrics, business intelligence, tracking?
My personal preference is towards data immutability and persistence where possible so I would move toward that kind of solution, but that’s obviously a matter for a much wider discussion taking into account performance, business needs, infrastructure, cost, etc.

We could also implement some solution to keep track of all data changes and enable convenient rollbacks.


# Answers

## 	Why can we not easily split this project into two micro-services?

As we uncovered in previous part, we can’t easily split app into two micro services due to data dependency between models, but even after clearing that we still end up with data model related logic passing through layers and making it difficult to unwind service related logic without touching the other one. Once our domain relevant repos are neatly nested where they should and there is not a single import across those parts we can start to think about splitting.After a quick glance, I did not see any common data or types dependency between user and item part, but in case there is one, we should plan introducing shared library or interface that they are going to use before creating autonomous services.

## 	Why does this project not adhere to the clean architecture even though we have separate modules for api, repositories, use cases and the model?

File structure is not an app architecture, we need to evaluate dependencies and abstraction layers to understand how clean it is. Clean architecture promotes decoupling of business logic from interfaces and specific implementations. Changes in outer layer should not result in need to adjust the inner one.This application does not create enough of later separation and entities independent of database implementation to call it clean. As we have seen in previous part during investigation, we are quite far from getting there.

## What would be your plan to refactor the project to stick to the clean architecture?

Some items were laid out already before, but lets create a simple roadmap:
- Create entities on which the use cases operate and which repositories depend on
- Abstract repositories away and use concrete ones injected through interfaces
- Rewrite use cases as functions that use injected repo and entities and are tested in isolation
- Rewrite API layer to use new use cases and provide configuration for concrete repo instances
- Clean up all code between domains and remove cross-boundary dependencies

Also, I would consider thinking more deliberately about domain design and structuring entities. For example, User is a very vague and easily misunderstood concept that could be misused across domains and use cases. Maybe it would be worth to distinguish between Customer and Staff or Admin on entity level, even if is stored in similar fashion in our database or share large portion of code for reduced redundancy? It would make it harder to use incorrectly and we could share only data relevant to particular role in the system in business logic entity.

I also think that hardcoding in form data dependencies between tables current business logic requirements is quite often not the most future-proof way of developing the app. We can’t predict everything and avoid any substantial changes in the future, but we could avoid setting 1 to 1 relationship between User and Cart in case we might want to implement features that would break that relationship. This is obviously very dependent on business plan, product design, etc. It is very hard to judge those kind of things and make premature calls from a very rudimentary example.

We might want to introduce DTOs, but this is a separate topic with a lot of considerations.

We should also not forget about the importance of reliable testing through the refactoring and restructuring part. I would:
- Write repositories and test them with temporary test db in test suite designed to check if we are correctly handling data persistence and all edge cases
- Write use cases and test them in isolation using mocks or in-memory implementation for repositories. At this stage we should closely mimic business requirements and user scenarios.
- Consider doing end to end testing for API layer and integration, including error cases, also we could use it for tracking regression and even use for acceptance testing. I would even consider doing quick snapshot testing locally to easily and cheaply ensure consistent behavior, apart from more QA focused black box testing

We could also introduce static code analysis that ensures that we do not introduce unwanted dependencies between domains, before we are able to finally split.

Bigger refactoring efforts (which is not in our toy example) also require coordination and planning between teams to make sure we are aligned on a goal and do not implement new features or do other braking changes while the effort is undertaken. Potential screening of product design and discussions between teams might be necessary.

# Requirements not met

Unfortunately I can see that requirements are not met, we are unable to provide customer with full registration process, do not include any authentication, roles, permissions.
We also do not have a role for inventory manager, etc.
I understand that this is for a simplicity of solution to work with on a tight time budget, but those are very important gaps that would require smart logic structuring to avoid breaking clean architecture and also introduce some important domain questions.