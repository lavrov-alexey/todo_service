import React from 'react';
import axios from 'axios';
import './App.css';
import UserList from "./components/User.js";
import ProjectList from "./components/Project.js";
import TodoList from "./components/Todo.js";
import ProjectTodoList from "./components/ProjectTodo"
import LoginForm from "./components/LoginForm";
import TodoForm from "./components/TodoForm";
import ProjectForm from "./components/ProjectForm";
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
            'token': '',
        }
    }

    isAuth() {
        // первый ! - преобразует в js в bool-тип, а второй ! - инвертирует полученный bool
        // если ключа token вообще нет в локал сторадже, то вернется не '', а undefined, поэтому нужен перевод в bool
        return !!this.state.token
    }

    // метод для проброса внутрь компонента ЛогинФорм и вытаскивания оттуда введенных пользователем логина и пароля
    obtainAuthToken(login, password) {
        // console.log('obtainAuthToken:', login, password)

        // направляем post запрос с логином и паролем для получения токена из бэка
        axios
            .post('http://localhost:8000/api-auth-token/', {
                "username": login,
                "password": password,
            })
            .then(response => {
                const token = response.data.token
                // console.log('token: ', token)

                // сохраняем полученный токен в локальном хранилище (более современный вариант, чем cookies
                localStorage.setItem('token', token)

                // setState - асинхронная функция и чтобы дождаться установки в состоянии токена пользователя и только
                // потом делать запросы уже с токеном - нужно 2ым параметром передать колл-бэк функции, которая будет
                // вызвана только после завершения работы функции setState
                this.setState({
                    'token': token,
                }, this.getData)
            })
            .catch(error => {
                console.log(error)
                alert("При попытке получения токена по логину и паролю - возникла ошибка:\n\n" + error)
            })

    }

    createProject(name, repo_link, users) {
        console.log(name, repo_link, users)

        let headers = this.getHeaders()  // получаем заголовки для запросов

        axios
            //полная запись передачи заголовков: {'headers': headers}, но можно передать короче, т.к. назв. поля то же
            .post('http://localhost:8000/api/projects/',
                {'name': name, 'repo_link': repo_link, 'users': users},
                {headers})
            .then(response => {
                // возможны 2 варианта - создавать сущность на фронте, дублируя логику бэка - усложнение схемы
                // или просто перечитать все данные из бэка снова - медленнее, но надежнее. Идем по варианту 2
                this.getData()
            })
            .catch(error => {
                // если ошибка (например 403 - доступ запрещен или что-то еще) - ошибку в консоль и вывод на экран
                console.log(error)
                alert("При попытке создания проекта возникла ошибка:\n\n" + error)
            })
    }

    componentDidMount() {
        // первым делом - поднимаем токен из закрытого локального хранилища (если он там есть)
        let token = localStorage.getItem('token')
        // и сохраняем его в текущем состоянии и только после этого - запрашиваем данные из бэка
        this.setState({
            'token': token,
        }, this.getData)
    }

    getHeaders() {
        // если токен в состоянии уже есть (авторизованы) - отдаем заголовок с ним, иначе - пустой объект
        if (this.isAuth()) {
            return {
                'Authorization': 'Token ' + this.state.token
            }
        }
        return {}
    }

    getData() {
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

        // получаем заголовки для запросов
        let headers = this.getHeaders()

        axios
            //полная запись передачи заголовков: {'headers': headers}, но можно передать короче, т.к. назв. поля то же
            .get('http://localhost:8000/api/users/', {headers})
            .then(response => {
                // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
                // const users = response.data.results
                const users = response.data
                this.setState({'users': users})
            })
            .catch(error => {
                // если ошибка (например 403 - доступ запрещен) - печатаем ошибку и сбрасываем данные в текущ. состоянии
                console.log(error)
                this.setState({'users': []})
                alert("При запросе данных пользователей с сервера возникла ошибка:\n\n" + error)
            })

        axios
            .get('http://localhost:8000/api/projects/', {headers})
            .then(response => {
                // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
                // const projects = response.data.results
                const projects = response.data
                this.setState({'projects': projects})
            })
            .catch(error => {
                // если ошибка (например 403 - доступ запрещен) - печатаем ошибку и сбрасываем данные в текущ. состоянии
                console.log(error)
                this.setState({'projects': []})
                alert("При запросе данных по проектам с сервера возникла ошибка:\n\n" + error)
            })

        axios
            .get('http://localhost:8000/api/todo/', {headers})
            .then(response => {
                // если используем в беке пагинацию - результат глубже - в results, если не используем, то просто в data
                // const todos = response.data.results
                const todos = response.data
                this.setState({'todos': todos})
            })
            .catch(error => {
                // если ошибка (например 403 - доступ запрещен) - печатаем ошибку и сбрасываем данные в текущ. состоянии
                console.log(error)
                this.setState({'todos': []})
                alert("При запросе данных по заметкам с сервера возникла ошибка:\n\n" + error)
            })
    }

    // при разлогинивании - гасим токен и перечитываем заново данные из бэка
    logOut() {
        localStorage.setItem('token', '')
        this.setState({
            'token': '',
        }, this.getData)
    }

    render() {
        return (
            <div className="sub_body">
                <div className="top App_header">
                    {/*меню из отдельного компонента*/}
                    {/*<Menu />*/}
                    <hr></hr>

                    {/*при использовании HashRouter: http://localhost:3000/#/users*/}
                    {/*при использовании BrowserRouter: http://localhost:3000/users*/}
                    <BrowserRouter>
                        <nav>
                            <li><Link to='/'>Список проектов</Link></li>
                            <li><Link to='/create_project'>Создать проект</Link></li>
                            <li><Link to='/todo'>Список записей</Link></li>
                            <li><Link to='/create_todo'>Создать запись</Link></li>
                            <li><Link to='/users'>Список пользователей</Link></li>
                            {/*В зависимости от того залогинен или нет - показываем разные кнопки*/}
                            <li> {
                                this.isAuth()
                                    ? <button onClick={() => this.logOut()}>Выйти</button>
                                    : <Link to='/login'>Войти</Link>
                            }
                            </li>
                        </nav>

                        <Routes>
                            {/*включаем локальный роутинг SPA на стороне клиента*/}
                            <Route exact path='/' element={<Navigate to='/projects'/>}/>
                            {/*прокидываем в компонент коллбэк функции, чтобы вытащить логин, пароль оттуда*/}
                            <Route exact path='/login' element={<LoginForm
                                obtainAuthToken={(login, password) => this.obtainAuthToken(login, password)}/>}/>
                            <Route exact path='/users' element={<UserList users={this.state.users}/>}/>
                            <Route exact path='/todo' element={<TodoList todos={this.state.todos}/>}/>
                            {/*передаем список пользователей в компонент для выбора допущенных к проекту и коллбек
                             функции создания проекта в компонент*/}
                            <Route exact path='/create_project' element={<ProjectForm
                                users={this.state.users}
                                createProject={(name, repo_link, users) => this.createProject(name, repo_link, users)}
                            />}/>
                            <Route exact path='/create_todo' element={<TodoForm projects={this.state.projects}/>}/>
                            {/*создаем динам. путь для вывода всех заметок конкретного проекта*/}
                            <Route path='/projects'>
                                <Route index element={<ProjectList projects={this.state.projects}/>}/>
                                <Route path=':projectId' element={<ProjectTodoList todos={this.state.todos}/>}/>
                            </Route>
                            {/*добавляем обработку несуществующих в приложении путей*/}
                            <Route path='*' element={<PageNotFound/>}/>

                        </Routes>
                    </BrowserRouter>
                </div>
                <div className="footer">
                    <hr></hr>
                    <Footer/>
                </div>
            </div>
        );
    }
}

export default App;
