
# Todo API

This is an API to save user info and save todos of those user on backend database

## Screenshots

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-signup.png)

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-token.png)

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-save-unauthorized.png)

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-save.png)

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-todo-list.png)

![App Screenshot](https://github.com/DeepProgram/Todo-API/raw/images/todo-api-update.png)



## Deployment Todo Endpoints

To deploy this project run below command in the cloned folder

```bash
  uvicorn main:app --reload --port=8000
```
- This will run the main api that handle all todo related task



## Deployment Authorization Endpoints

To deploy this project run below command in the cloned folder

```bash
  uvicorn auth.auth:app --reload --port=9000
```
- This will run the auth api that handle all authorization related task


## Authors

- [@DeepProgram](https://github.com/DeepProgram)

