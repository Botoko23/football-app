import {getData, play} from './index.js';

async function fetchData(season, league) {
    try {
        // Make a fetch request
        const response = await fetch(`https://la6j1cgnah.execute-api.us-east-1.amazonaws.com/dev/football?season=${season}&league=${league}`);

        // Check if the response status is OK (200-299)
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        }
        // Parse the response as JSON
        const data = await response.json();

        // Process the data
        const clubs = Object.keys(data);
        const points = Object.values(data);
        const startingPts = [];
        for (let i = 0; i < clubs.length; i++) {
            startingPts.push(points[i][0])
            
        };

        return {
            clubs: clubs,
            points: points,
            startingPts: startingPts
        };

    } catch (error) {
        // Handle errors
        console.error('Error fetching data:', error.message);
    }
}



// setup 
const data = {
    labels: null,
    datasets: [{
        label: 'Racing bar chart',
        data: null,
        backgroundColor: null,
        borderWidth: 0.7
    }]
};

// config 
const config = {
    type: 'bar',
    data,
    options: {
        indexAxis: "y",
        scales: {
        x: {
            beginAtZero: true
        }   
        },

    }
};

// render init block
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);


const clubColors = {
    "Premier-League": 20,
    "La-Liga": 20,
    "Ligue-1": 18,
    "Serie-A": 20,
    "Bundesliga": 18, 

    generateColors: function (league){
        // Generate a random hex value between 0 and 255 for each RGB component
        let randomColors = []
        for (let i = 0; i < this[league]; i++) {
            let randomColorComponent = () => Math.floor(Math.random() * 256);

            let red = randomColorComponent();
            let green = randomColorComponent();
            let blue = randomColorComponent();
      
            // Concatenate the RGB components to form an RGB color
            let rgbColor = `rgb(${red}, ${green}, ${blue})`;


            randomColors.push(rgbColor);
        }
        return randomColors;
    }
} ;


export async function animateChart(season, league){
    let ptsIdx = 0
    const colors = clubColors.generateColors(league)
 

    const {clubs, points, startingPts} = await fetchData(season, league)

    // const matchWks = points[0].length 
    const timeOut =  points[0].length  * 500

    myChart.config.data.labels = clubs;
    myChart.config.data.datasets[0].data = startingPts;
    myChart.config.data.datasets[0].backgroundColor = colors;

    
    play.classList.remove('hidden')
    getData.classList.add('hidden')
    
    function updateChart() {

        let merged = myChart.config.data.labels.map((label, i) => {
            return {
                'labels': myChart.config.data.labels[i],
                'dataPoints': myChart.config.data.datasets[0].data[i],
                'backgroundColor': myChart.config.data.datasets[0].backgroundColor[i],
            }
        });
    
        const lab = [];
        const dp = [];
        const bgc = [];
    
        const dataSort = merged.sort((b, a) => {
            return a.dataPoints - b.dataPoints
        })
    
        for (let i = 0; i < dataSort.length; i++) {
            lab.push(dataSort[i].labels);
            dp.push(dataSort[i].dataPoints);
            bgc.push(dataSort[i].backgroundColor);
        };
        
        ptsIdx++

        myChart.config.data.labels = lab;
        myChart.config.data.datasets[0].data = dp;
        myChart.config.data.datasets[0].backgroundColor = bgc;
        myChart.config.data.datasets[0].label = `Matchday ${ptsIdx}`
            
        myChart.update()
        console.log(dp)


        if (ptsIdx <= points[0].length) {
            for (let index = 0; index < clubs.length; index++) {
                dp[lab.indexOf(clubs[index])] = points[index][ptsIdx]
            };
        };

        if (ptsIdx === points[0].length){
            getData.classList.remove('hidden')
        }

    
    };


    play.classList.remove('hidden')


    play.addEventListener('click', () => {
        play.classList.add('hidden')
        const myInterval = setInterval(updateChart, 500);
        setTimeout(function() {
            clearInterval(myInterval);
        }, timeOut);
    });
};




