
document.addEventListener('DOMContentLoaded', ()=>{
    x = document.querySelectorAll(".btn-outline-primary");
    console.log(x)
    x.forEach(element => {
        console.log(element)

        element.style.color = 'maroon';
        element.style.borderColor = 'darkgoldenrod';

        element.addEventListener('mouseenter', ()=>{
            element.style.backgroundColor = 'black';
            element.style.color = 'white';
            element.style.borderColor = 'red';
        })

        element.addEventListener('mouseleave', ()=>{
            element.style.color = 'maroon';
            element.style.borderColor = 'darkgoldenrod';
            element.style.backgroundColor = 'transparent';
        })

        element.addEventListener('mousedown', ()=> {
            element.style.borderColor = 'red';
        })
    });
})