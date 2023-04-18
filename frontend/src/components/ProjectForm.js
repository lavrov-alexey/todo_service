import React from 'react';

class ProjectForm extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          'name': '',
          'repo_link': '',
          'users': []
      }
  }

  // локальный обработчик на событие изменения полей ввода логин, пароль
  handleChange(event) {
      this.setState({
          // при изменении поля ввода - мы сохраняем введенное в состояние соотв. поля
          [event.target.name]: event.target.value
      })
  }

  //обработчик на выбор в мультиселекте допущенных к проекту пользователей
  handleUsersSelect(event) {
      if (!event.target.selectedOptions) {  // если ничего не выбрал - очищаем локальный список пользователей
          this.setState({
              'users': []
          })
          return;
      }

      // если что-то было выбрано - обходим все выбранные options и сохраняем id выбранных пользователей в лок. state
      let selected_users = []
      for(let option of event.target.selectedOptions) {
          selected_users.push(option.value)
      }
      this.setState({
          'users': selected_users
      })
  }

  // локальный обработчик на событие отправки формы логина
  handleSubmit(event) {
      this.props.createProject(this.state.name, this.state.repo_link, this.state.users)
      // console.log(this.state.name, this.state.repo_link, this.state.users)
      // останавливаем действия браузера по-умолчанию, чтобы не обновлялась стр. и не отправлялся get-запрос
      event.preventDefault()
  }

    render() {
      return (
          <div>
              <form onSubmit={(event) => this.handleSubmit(event)}>
                  <input type="text" name="name" placeholder="name" value={this.state.name}
                         onChange={(event) => this.handleChange(event)} />
                  <input type="text" name="repo_link" placeholder="repo_link" value={this.state.repo_link}
                         onChange={(event) => this.handleChange(event)} />
                  {/*далее нужен мультиселект для выбора пользователей создаваемого проекта*/}
                  <select multiple onChange={(event) => this.handleUsersSelect(event)}>
                      {/*формируем для каждого из переданного в компонент списка пользователей строку для select*/}
                      {this.props.users.map((user) =>
                          <option value={user.id}>{user.last_name} {user.first_name}</option>)}
                  </select>
                  <input type="submit" value="Создать" />
              </form>
          </div>
      );
  }
}

export default ProjectForm;
