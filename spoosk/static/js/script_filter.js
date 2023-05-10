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
        console.log('1')
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