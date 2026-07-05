document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('graficoMontajes').getContext('2d');
    let graficoActual;
    
    // Los datos se pasarán desde la plantilla
    
    const opciones = {
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        },
        responsive: true,
        maintainAspectRatio: false
    };
    
    function mostrarGrafico(datos) {
        if (graficoActual) {
            graficoActual.destroy();
        }
        
        graficoActual = new Chart(ctx, {
            type: 'line',
            data: datos,
            options: opciones
        });
    }
    
    // Inicializar con los datos de la semana
    window.inicializarGrafico = function(datosSemanales, datosMensuales, datosTrimestre) {
        // Mostrar gráfico semanal por defecto
        mostrarGrafico(datosSemanales);
        
        // Botones para cambiar el período
        document.getElementById('btn-semana').addEventListener('click', function() {
            actualizarBotones(this);
            mostrarGrafico(datosSemanales);
        });
        
        document.getElementById('btn-mes').addEventListener('click', function() {
            actualizarBotones(this);
            mostrarGrafico(datosMensuales);
        });
        
        document.getElementById('btn-trimestre').addEventListener('click', function() {
            actualizarBotones(this);
            mostrarGrafico(datosTrimestre);
        });
    };
    
    function actualizarBotones(botonActivo) {
        document.querySelectorAll('.filter-button').forEach(btn => {
            btn.classList.remove('active');
        });
        
        botonActivo.classList.add('active');
    }
});
