import {animateChart} from './animation.js';

let season, league;


const dropDownBtn1 = document.querySelector(".dropdown-toggle1")
const dropDownMenu1 = document.querySelector(".dropdown-menu1")

const dropDownBtn2 = document.querySelector(".dropdown-toggle2")
const dropItem2 = document.querySelectorAll(".dropdown-item2")

export const getData = document.querySelector("#getData")
export const play = document.querySelector("#play")
// const info = document.getElementById('info')
// const chart = document.getElementById('myChart')


function removeElements(){
    const oldLi = document.querySelectorAll('.dropdown-item1')
    oldLi.forEach(element => {
        element.remove();
    });
        
};


dropDownBtn1.addEventListener("click", function() {
    removeElements();
    for (let i = 0; i < 20; i++) {
        const today = new Date();
        let currentYear = today.getFullYear();
        const li = document.createElement('li');
        li.classList.add('dropdown-item', 'dropdown-item1');
        const seasonText = `${currentYear - (i + 1)}-${currentYear - i}`;
        li.innerText = seasonText;
  
        li.addEventListener('click', () => {
            season = li.innerText;
            console.log(season);
          
        });

        dropDownMenu1.appendChild(li); 
    }
})


dropItem2.forEach(item => {
    item.addEventListener('click', () => {
        league = item.innerText.replace(" ", "-");
        console.log(league);
    })    
});


getData.addEventListener('click', () => {

    try {
        // Some code that might throw an error
        if (season !== null && league !== null){
            animateChart(season, league);
            getData.classList.add('hidden');
        }else{
            throw new Error("Please select the league and season");
        }

    } catch (error) {
        // Catch and handle the error
        alert("An error occurred: " + error.message);
    }

})












