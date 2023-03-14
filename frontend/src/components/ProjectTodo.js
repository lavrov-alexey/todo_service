import React from 'react';
import {useParams} from 'react-router-dom'

const ProjectTodoItem = ({todo}) => {

    return (
        <tr>
            <td>
                {todo.project}
            </td>
            <td>
                {todo.todo_text}
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

const ProjectTodoList = ({todos}) => {
    // используя функцию - получаем параметры и отбираем заметки, относящиеся к переданному id проекта
    let params = useParams()
    let filteredTodos = todos.filter((todo) => todo.project === parseInt(params.projectId))

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
            {filteredTodos.map((todo) => <ProjectTodoItem todo={todo} />)}
        </table>
    )
}

export default ProjectTodoList