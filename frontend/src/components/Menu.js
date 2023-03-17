// import React from "react";
//
// const MenuContainer = () => {
//     return(
//         <div>
//             <table>
//                 <th>Users List</th>
//                 <th>TODOs List</th>
//                 <th>Projects List</th>
//             </table>
//         </div>)
// }
//
// export default MenuContainer

import React from "react";
import {Container, Navbar} from "react-bootstrap"
import {Link} from "react-router-dom";

const Menu = () => {
    return (
        <header>
            <Navbar bg="dark" variant="dark" expand="lg">
                <Container>
                    <th><Navbar.Brand href="#">Users list</Navbar.Brand></th>
                    <th> | </th>
                    <th><Navbar.Brand href="#">Projects list</Navbar.Brand></th>
                    <th> | </th>
                    <th><Navbar.Brand href="#">TODOs list</Navbar.Brand></th>
                </Container>
            </Navbar>
        </header>
    )
}

export default Menu