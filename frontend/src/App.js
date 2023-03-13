import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import UserList from "./components/User.js";
import ProjectList from "./components/Project.js";
import TodoList from "./components/Todo.js";
import Menu from "./components/Menu";
import Footer from "./components/Footer";

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
                <Menu />
                <hr></hr>
                <UserList users={this.state.users}/>
                <ProjectList projects={this.state.projects}/>
                <TodoList todo={this.state.todo}/>
              </div>
              <div className="footer">
                  <hr></hr><Footer />
              </div>
          </div>
      );
  }
}

export default App;
