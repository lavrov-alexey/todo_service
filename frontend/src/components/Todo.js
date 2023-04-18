import React from 'react';

const TodoItem = ({todo}) => {
    return (
        <tr>
            <td>
                {todo.project}
            </td>
            <td>
                {todo.todo_text}
            </td>
            <td>
                {/*{this.props.users[1]}*/}
                {todo.creator}
            </td>
            {/*<td>*/}
            {/*    {todo.is_active}*/}
            {/*</td>*/}
            {/*<td>*/}
            {/*    {todo.created_at}*/}
            {/*</td>*/}
            {/*<td>*/}
            {/*    {todo.updated_at}*/}
            {/*</td>*/}
            {/*<td>*/}
            {/*    {todo.is_deleted}*/}
            {/*</td>*/}
        </tr>
    )
}

const TodoList = ({todos, users}) => {
    console.log(todos)
    console.log(users)

    return (
        <table>
            <th>
                Project
            </th>
            <th>
                Text
            </th>
            <th>
                Author
            </th>
            {/*<th>*/}
            {/*    Is active*/}
            {/*</th>*/}
            {/*<th>*/}
            {/*    Created at*/}
            {/*</th>*/}
            {/*<th>*/}
            {/*    Updated at*/}
            {/*</th>*/}
            {/*<th>*/}
            {/*    Is deleted*/}
            {/*</th>*/}
            {todos.map((todo) => <TodoItem todo={todo}/>)}
        </table>
    )
}

export default TodoList