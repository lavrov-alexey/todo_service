import React from 'react';

const TodoItem = ({todo}) => {

    return (
        <tr>
            <td>
                {todo.project}
            </td>
            <td>
                {todo.text}
            </td>
            <td>
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

const TodoList = ({todos}) => {

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
            {todos.map((todo) => <TodoItem todo={todo} />)}
        </table>
    )
}

export default TodoList