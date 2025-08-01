// main.js

function showSection(sectionId, element) {
    // Ocultar todas las secciones de contenido
    document.querySelectorAll('.content-section').forEach(function(section) {
        section.classList.add('hidden');
    });
    
    // Quitar la clase 'active' de todos los botones de navegación
    document.querySelectorAll('.nav-button').forEach(function(button) {
        button.classList.remove('active');
    });

    // Mostrar la sección seleccionada
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.classList.remove('hidden');
    }

    // Añadir la clase 'active' al botón que fue presionado
    if (element) {
        element.classList.add('active');
    }
}

// Se ejecuta cuando el contenido de la página ha cargado
document.addEventListener('DOMContentLoaded', function() {
    // Mostrar la primera sección por defecto
    const firstButton = document.querySelector('.nav-button');
    showSection('quienes-somos', firstButton);
});