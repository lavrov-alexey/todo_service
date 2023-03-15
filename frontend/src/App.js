import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import UserList from "./components/User.js";
import ProjectList from "./components/Project.js";
import TodoList from "./components/Todo.js";
import ProjectTodoList from "./components/ProjectTodo"
import {HashRouter, BrowserRouter, Route, Routes, Link, Navigate, useLocation}
    from 'react-router-dom'
import Menu from "./components/Menu";
import Footer from "./components/Footer";


const PageNotFound = () => {
  // распаковываем из полученного объекта путь страницы, откуда пришли сюда в лок. переменную
  let {pathname} = useLocation()

  return (
      <div>
          Page "{pathname}" not found!
      </div>
  )
}

class App extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          'users': [],
          'projects': [],
          'todos': [],
      }
  }

  componentDidMount() {
      // заглушка со статичными данными
      // const users = [
      //     {
      //         'username': 'Tst-1',
      //         'last_name': 'LN_Test-1',
      //         'first_name': 'FN_Test-1',
      //         'email': 'test1@mail.ru'
      //     },
      //     {
      //         'username': 'Tst-2',
      //         'last_name': 'LN_Test-2',
      //         'first_name': 'FN_Test-2',
      //         'email': 'test2@mail.ru'
      //     },
      // ]

      axios
          .get('http://localhost:8000/api/users/')
          .then(response => {
              // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
              const users = response.data.results
              this.setState(
                  {
                    'users': users
                    }
            )
          })
          .catch(error => console.log(error))

      axios
          .get('http://localhost:8000/api/projects/')
          .then(response => {
              // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
              const projects = response.data.results
              this.setState(
                  {
                    'projects': projects
                    }
            )
          })
          .catch(error => console.log(error))

      axios
          .get('http://localhost:8000/api/todo/')
          .then(response => {
              // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
              const todos = response.data.results
              this.setState(
                  {
                    'todos': todos
                    }
            )
          })
          .catch(error => console.log(error))
  }

    render() {
      return (
          <div className="sub_body">
              <div className="top App_header">
                {/*меню из отдельного компонента*/}
                {/*<Menu />*/}
                <hr></hr>
                  <BrowserRouter>
                      <nav>
                          <li> <Link to='/'>Project list</Link> </li>
                          <li> <Link to='/todo'>ToDo list</Link> </li>
                          <li> <Link to='/users'>User list</Link> </li>
                      </nav>

                    <Routes>
                      {/*включаем локальный роутинг SPA на стороне клиента*/}
                      <Route exact path='/' element={<Navigate to='/projects' />} />
                      <Route exact path='/users' element={<UserList users={this.state.users} />} />
                      <Route exact path='/todo' element={<TodoList todos={this.state.todos} />} />
                      {/*создаем динам. путь для вывода всех заметок конкретного проекта*/}
                      <Route path='/projects'>
                        <Route index element={<ProjectList projects={this.state.projects} />} />
                        <Route path=':projectId' element={<ProjectTodoList todos={this.state.todos} />} />
                      </Route>
                      {/*добавляем обработку несуществующих в приложении путей*/}
                      <Route path='*' element={<PageNotFound />} />

                    </Routes>
                  </BrowserRouter>
              </div>
              <div className="footer">
                  <hr></hr><Footer />
              </div>
          </div>
      );
  }
}

export default App;
