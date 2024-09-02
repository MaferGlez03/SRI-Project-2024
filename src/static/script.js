document.getElementById('config-button').addEventListener('click', function() {
    var configOptions = document.getElementById('config-options');
    var searchResults = document.getElementById('search-results');

    if (configOptions.classList.contains('hidden')) {
        configOptions.classList.remove('hidden');
        searchResults.classList.add('hidden');
    } else {
        configOptions.classList.add('hidden');
        searchResults.classList.remove('hidden');
    }
});


document.getElementById('search-form').addEventListener('submit', function(event) {
    var option1 = document.getElementById('option1');
    if (option1.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'option1';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    if (query_expand_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'query_expand_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    if (stop_words_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'stop_words_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }

    if (stemmer_bool.checked) {
        var hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'stemmer_bool';
        hiddenField.value = 'true';
        this.appendChild(hiddenField);
    }


    var query = document.querySelector('input[name="search"]').value;
    var words = query.split(' ');
    var sliderValues = [];

    words.forEach(function(word, index) {
        var slider = document.getElementById('slider-' + index);
        if (slider) {
            sliderValues.push(slider.value);
        }
    });

    var sliderField = document.createElement('input');
    sliderField.type = 'hidden';
    sliderField.name = 'sliders';
    sliderField.value = JSON.stringify(sliderValues);
    this.appendChild(sliderField);
});

document.querySelector('input[name="search"]').addEventListener('input', function() {
    var query = this.value;
    var words = query.split(' ');
    var slidersContainer = document.getElementById('sliders-container');
    slidersContainer.innerHTML = '';

    words.forEach(function(word, index) {
        var sliderLabel = document.createElement('label');
        sliderLabel.textContent = `Valor del Slider para "${word}" (-1 a 1): `;
        var sliderValue = document.createElement('span');
        sliderValue.id = 'slider-value-' + index;
        sliderValue.textContent = '0';

        var slider = document.createElement('input');
        slider.type = 'range';
        slider.id = 'slider-' + index;
        slider.name = 'slider-' + index;
        slider.min = '-1';
        slider.max = '1';
        slider.step = '0.01';
        slider.value = '0';
        slider.addEventListener('input', function() {
            sliderValue.textContent = this.value;
        });

        slidersContainer.appendChild(sliderLabel);
        slidersContainer.appendChild(sliderValue);
        slidersContainer.appendChild(slider);
        slidersContainer.appendChild(document.createElement('br'));
    });
});

// Almacenar los valores iniciales de los sliders
var initialSliderValues = [];
document.querySelectorAll('input[type="range"]').forEach(function(slider, index) {
    initialSliderValues.push(slider.value);
});

// Manejar el reseteo de los sliders
document.getElementById('reset-button').addEventListener('click', function() {
    document.querySelectorAll('input[type="range"]').forEach(function(slider, index) {
        slider.value = initialSliderValues[index];
        document.getElementById('slider-value-' + index).textContent = initialSliderValues[index];
    });
});

document.getElementById('option1').addEventListener('change', function() {
    var slidersContainer = document.getElementById('sliders-container');
    var resetButton = document.getElementById('reset-button');
    
    if (this.checked) {
        slidersContainer.style.display = 'block';
        resetButton.style.display = 'block';
    } else {
        slidersContainer.style.display = 'none';
        resetButton.style.display = 'none';
    }
});

window.onload = function() {
    var option1 = document.getElementById('option1');
    var slidersContainer = document.getElementById('sliders-container');
    var resetButton = document.getElementById('reset-button');
    
    if (!option1.checked) {
        slidersContainer.style.display = 'none';
        resetButton.style.display = 'none';
    }
};


