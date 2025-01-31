# Prompt Examples

These are examples of prompts that we can send.
These prompts have different levels of complexity based on the quality of the LLM response. The higher the level, the harder it is for the LLM to understand what it needs to respond.
Some levels may have more than 1 example.

### Level 1

Ask to add the fields `updated_at` and `created_at` to the `User` model.
It includes the django migration with the changes and tests for the functionality.

```
  We need to add two fields, created_at and updated_at, to the User model to track when a user account is created and last updated. These fields will be automatically populated by Django using the auto_now and auto_now_add options.\n\ncreated_at should be set when the User is created.\nupdated_at should automatically update whenever the User instance is saved.\n\nThe created_at field is automatically set when a new User is created and should not be modified after creation.\nThe updated_at field is automatically updated every time the User model is saved.\nThe fields should be added to the database schema via a migration.\nThere should be no impact on the existing functionality of the User model.\n\nWrite some tests to ensure that the created_at field is set only once and does not change after creation, and that updated_at changes after saving the model.\nThere should be no impact on existing tests, if you are to add a test to an existing file, do so at the end of the file.
```

### Level 2

Ask to add a custom manager to the `User` model that filters users that have a first name and a last name.
It includes tests for the functionality.

```
We need to add a custom manager to the User model that filters users that have a non-empty value for the fields name_first and name_last. This custom manager will provide a method called named_users, which returns only users where name_first and name_last are not Null and not empty string.\nThe named_users method should allow you to easily query the User model for only named users, while still preserving the default behavior of the model.\nThe custom manager should be added to the User model and should not affect any existing functionality or queries on the User model unless explicitly called.\nThe custom manager should be implemented using Django’s Manager class and should be included in the model’s default manager field.\nWrite some tests to ensure that the active_users method returns only users where name_first and name_last are not Null and not empty, and does not include users with first or last names. Also, make sure that existing queries that don’t use the custom manager still work as expected, and that the addition of the custom manager has no impact on the functionality of the User model.\nThere should be no impact on existing tests. If you add a test to an existing test file, please add it at the end of the file.
```

Ask to refactor a function to improve readability.
It includes tests for the functionality.

```
We need to refactor the function picture_creation in the file mutations.py to improve its readability and maintainability. The function currently handles multiple responsibilities, which makes it harder to understand and modify. The goal is to break the function into smaller, more manageable parts, each responsible for a single task.\n\nThe refactored code should keep the same behavior as the original function and should not introduce any new bugs or change its output. The main objective is to improve the clarity of the function and make it easier for developers to work with in the future.\n\nThe refactor should involve:\nBreaking down the large function into smaller, self-contained helper functions that each perform a single task.\nRenaming variables and functions to use more descriptive and meaningful names that clearly indicate their purpose.\nSimplifying any complex logic or conditionals, while ensuring that the function remains efficient.\nRemoving any unnecessary code, comments, or duplication.\nThe function’s overall behavior should remain unchanged after the refactor, but the code should now be easier to read, understand, and extend in the future.\n\nWrite tests to ensure that the refactored function performs the same as the original. There should be no impact on existing tests, and if you are to add a test to an existing file, please do so at the end of the file.
```

### Level 3

Ask to remove a field from a model and create a migration to update the database.
It includes tests for the functionality.

```
We need to remove the user_handle field from the User model that is no longer in use. This field should be entirely removed from the model, the database schema and any other components like queries, mutations or input types.\n\nThe field should be safely removed, and the database schema should be updated accordingly via a new migration. The migration should ensure that the field is removed from the database without causing any issues for existing data or functionality.\n\nThe following steps should be followed:\n\nRemove the deprecated field from the User model.\nCreate and apply a migration that removes the field from the database schema.\nEnsure the model and migration are updated correctly so that the application continues to work as expected without any references to the deprecated field.\nAny data or functionality that previously relied on this field should be cleaned up, if applicable.\nOnce the field is removed, update any related code that referenced it, including readme's, serializers, mutations, queries, inputs, or any other components, to ensure that no references to the deprecated field remain in the codebase.\n\nWrite tests to ensure that the User model behaves correctly after the field is removed. There should be no impact on existing tests, and if you add a test to an existing file, please add it at the end of the file.
```

### Level 4

Ask to implement a many-to-many relationship with additional fields on the relationship.
It includes tests for the functionality.

```
We need to implement a many-to-many relationship between the existing User model and a new model, Group, with additional fields on the relationship to store extra data. This will involve creating a join table (intermediate model) that will store the relationship between the two models, along with 2 additional fields: role, role of the user on the group and joined_at, the date when the user joined the group.\nThe relationship should be implemented as follows:\n\nThe User model should have a many-to-many field to Group via the intermediate model.\nThe intermediate model should store the role and joined_at fields.\nThe intermediate model should include foreign keys to both User and Group, along with any extra fields necessary for the relationship.\nThe join table should be created via a migration, and the schema should be updated to reflect this new relationship.\n\nWrite tests to ensure that:\n\nThe many-to-many relationship between User model and Group model works correctly.\nThe additional fields on the join table are properly set and accessible.\nExisting functionality and data in User model and Group model are unaffected by the new relationship.\nThere should be no impact on existing tests. If you are adding a test to an existing file, please do so at the end of the file.
```

### Next steps

Some other examples that could be tested as more complex prompts (in complexity order):

- Implement custom validation in a serializer
- Replace a for loop with bulk_create() for performance improvement
- Create a custom database index to improve search performance
- Replace an in-memory query with a database query for scalability
- Implementing asynchronous tasks with Celery in a Django project
- Refactor to remove "magic strings" by using constants or enums
