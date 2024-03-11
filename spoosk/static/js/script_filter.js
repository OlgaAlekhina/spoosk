document.querySelectorAll('.form-group-content').forEach( function (dropDonwWrapper) {
    
    const dropDownBtn = dropDonwWrapper.querySelector('.dropdown-button');
    const dropDownList = dropDonwWrapper.querySelector('.dropdown-list');
    const dropDownListItems = dropDownList.querySelectorAll('.dropdown-list-item');
    const dropDownInput = dropDonwWrapper.querySelector('.dropdown-input-hidden');
    
    // Клик по кнопке открыть/закрыть
    dropDownBtn.addEventListener('click', function () {
        dropDonwWrapper.querySelector('.dropdown-list').classList.toggle('dropdown-list--visible')
        this.classList.add('dropdown-button--active')
    });

    // Выбор элемента из списка 
    dropDownListItems.forEach( function (listItem) {
        listItem.addEventListener('click', function(e) {
            e.stopPropagation();
            dropDownBtn.innerText = this.innerText;
            dropDownBtn.focus();
            dropDownInput.value = this.dataset.value;
            dropDownList.classList.remove('dropdown-list--visible');
        })
    });

    // клик снаружи. закрыть дропдаун
    document.addEventListener('click', function (e) {
        if (e.target !== dropDownBtn) {
            dropDownBtn.classList.remove('dropdown-button--active');
            dropDownList.classList.remove('dropdown-list--visible');
        }
    });
    
    // Нажатие на Tab или Escape
    dropDonwWrapper.addEventListener('keydown', function (e) {
        if (e.key === 'Tab' || e.key === 'Escape') {
            dropDownBtn.classList.remove('dropdown-button--active');
            dropDownList.classList.remove('dropdown-list--visible');
        }
    });
});

let range_inputs = document.getElementsByClassName("slider");
console.log(range_inputs);

for(var i = 0; i < range_inputs.length; i++) {
    range_inputs[i].addEventListener('input', function() {
    var value = (this.value-this.min)/(this.max-this.min)*100;
    this.style.background = 'linear-gradient(to right, #005FF9 0%, #005FF9 ' + value + '%, #7CB8FF ' + value + '%, #7CB8FF 100%)';
});
};

//console.log(document.querySelector(".search-slider"));

//document.querySelector(".search-slider").oninput = function() {
//  var value = (this.value-this.min)/(this.max-this.min)*100;
//  this.style.background = 'linear-gradient(to right, #005FF9 0%, #005FF9 ' + value + '%, #7CB8FF ' + value + '%, #7CB8FF 100%)';
//};