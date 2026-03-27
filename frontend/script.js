
boton = document.getElementById("searchFrom").addEventListener("submit", async function(e){
    e.preventDefault();

    const nombreInput = document.querySelector("input").value.trim()
    n = normalizar(nombreInput);

    const url = `http://localhost:8000/nombre/${nombreInput}`;

    data = await getData(url)
    if (data && data.anio){
        input.value = " ";
        grafico(data, n);
    } else {
        alert("No se encontraron datos para ese nombre.");
    }
})

async function getData(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Error en la red");
        const data = await response.json();
        return data;
    } catch (error) {
            console.error('Error:', error);
        }
    }

function normalizar(nombre){
   nombre = nombre.toUpperCase();
   reemplazos = new Map([
    ["Á", "A"], ["É", "E"], ["Í", "I"], ["Ó", "O"], ["Ú", "U"],
    ["À", "A"], ["È", "E"], ["Ì", "I"], ["Ò", "O"], ["Ù", "U"],
    ["Ü", "U"], ["Ï", "I"], 
    [".", ""], [",", ""]
   ])

   for(const [key,value] of reemplazos){
        nombre.replaceAll(value, key);
    }
        return nombre
}
   
function grafico(d,nombre){
    var data = [
       {
        x: d.anio.map(a => String(a)), //para que la variable sea categorica 
        y: d.porcentaje,
        customdata: d.cantidad, 
        type: "bar", 
        hovertemplate:`Nacieron <b>%{customdata}</b> personas con el nombre <b>${nombre}</b><br>`+
                      'Representa al <b>%{y:.2f}%</b> del total de nacidos ese año'+
                      '<extra></extra>'
        
       }
    ]
    const layout = {
        title: nombre,
        hovermode: "x unified",
        xaxis:{
            title:"Año",
            tickmode:"linear",
            tick0: 1925,
            dtick: 5,
            tickangle: -45,
            showgrid: true,       
            gridcolor: '#E2E2E2',
        },
        yaxis: {
            title: "Porcentaje de personas nacidas en argentina",
            showgrid: true,       
            gridcolor: '#E2E2E2' 
        }
    }
    const container = document.getElementById('graficoContainer');
    container.innerHTML = ''; // limpiar el mensaje de carga
    Plotly.newPlot('graficoContainer', data, layout);
};


    
