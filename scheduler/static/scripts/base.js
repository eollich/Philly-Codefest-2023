/*Expander Menu */
const showMenu = (toggleId, navbarId, bodyId) =>{
    const toggle = document.getElementById(toggleId)
    const navbar = document.getElementById(navbarId)
    const bodypadding = document.getElementById(bodyId)

    if(toggle && navbar){
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('expander')

            toggle.classList.toggle('bx-x')

            bodypadding.classList.toggle('body-pd')
        })
    }
}
showMenu('nav-toggle','navbar','body-pd')

/* Link Active */

const linkColor = document.querySelectorAll('.nav__link')
