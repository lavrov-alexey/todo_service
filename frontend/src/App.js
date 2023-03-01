import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import UsersList from "./components/User.js";
import MenuContainer from "./components/MenuContainer";
import FooterContainer from "./components/FooterContainer";

class App extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          'users': []
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
            this.setState(
          {
                    'users': response.data
                }
            )
          })
          .catch(error => console.log(error))
  }

    render() {
      return (
          // <MenuContainer />
          <div>
            <UsersList users={this.state.users}/>
          </div>
          // <FooterContainer />
      );
  }
}

export default App;
