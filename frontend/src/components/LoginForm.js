import React from 'react';

class LoginForm extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          'login': '',
          'password': '',
      }
  }

  // локальный обработчик на событие изменения полей ввода логин, пароль
  handleChange(event) {
      this.setState({
          // при изменении поля ввода - мы сохраняем введенное в состояние - поле логина или пароля
          [event.target.name]: event.target.value
      })
  }

  // локальный обработчик на событие отправки формы логина
  handleSubmit(event) {
      // console.log(this.state.login, this.state.password)
      // в метод основного компонента прокидываем из нашего компонента введенные пользователем логин и пароль
      this.props.obtainAuthToken(this.state.login, this.state.password)
      // останавливаем действия браузера по-умолчанию, чтобы не обновлялась стр. и не отправлялся get-запрос
      event.preventDefault()
  }

    render() {
      return (
          <div>
              <form onSubmit={(event) => this.handleSubmit(event)}>
                  <input type="text" name="login" placeholder="login" value={this.state.login}
                         onChange={(event) => this.handleChange(event)}
                  />
                  <input type="password" name="password" placeholder="password" value={this.state.password}
                         onChange={(event) => this.handleChange(event)}
                  />
                  <input type="submit" value="Login" />
              </form>
          </div>
      );
  }
}

export default LoginForm;
