if (document.querySelector('.black-length')) {
  // Получаем его содержимое, только если элемент с таким классом найден
  blackL = Number(document.querySelector('.black-length').textContent);
} else {
  blackL = 0;
}
if (document.querySelector('.red-length')) {
  redL = Number(document.querySelector('.red-length').textContent);
} else {
  redL = 0;
}
if (document.querySelector('.blue-length')) {
  blueL = Number(document.querySelector('.blue-length').textContent);
} else {
  blueL = 0;
}
if (document.querySelector('.green-length')) {
  greenL = Number(document.querySelector('.green-length').textContent);
} else {
  greenL = 0;
}

totalL = Number(document.querySelector('.total-length').textContent);

anychart.onDocumentReady(function () {
    // добавляем данные
    let data = anychart.data.set([
        ["Очень сложная трасса", blackL],
        ["Сложная трасса", redL],
        ["Трасса средней сложности", blueL],
        ["Лёгкая трасса", greenL]
    ]);
    drawChart(data, totalL);
});

function drawChart(data, totalL) {
    // создаем цветовую палитру
    let palette = anychart.palettes.distinctColors();

    // добавляем цвета в соответствии с брендами
    palette.items([
        { color: "#7B7B7B" },
        { color: "#EC818F" },
        { color: "#99DCED" },
        { color: "#ABE991" }
    ]);

    // создаем экземпляр круговой диаграммы с переданными данными
    let chart = anychart
        .pie(data)
        // настраиваем цветовую палитру
        .palette(palette)
        // устанавливаем внутренний радиус для создания кольцевой диаграммы
        .innerRadius("65%");
    // устанавливаем заголовок диаграммы
    //    chart
    //        .title()
    //        .enabled(true)
    //        .useHtml(true)
    //        .text(
    //            '<span style = "color: #2C2D2E; font-size:24px; line-height:28px; font-weight:700; margin-top:28px; margin-bottom:10px; dy:20px">Общая протяжённость и сложность трасс</span>'
    //        );

    // устанавливаем идентификатор контейнера для диаграммы
    chart.container("donut-chart");

    chart.labels().format(function() {
        let value = this.value/1000
        return Math.round(value)
    });
    chart.labels().fontSize(20).fontWeight(500).fontFamily('Raleway');
    chart.legend(false);


    // создание отдельной метки
    let label = anychart.standalones.label();
    label
        .useHtml(true)
        .text(
            `<span style="color: #2C2D2E; font-size:24px; line-height:28px; font-weight:700;">${totalL} км</span>`
        )
        .position("center")
        .anchor("center")
        .hAlign("center")
        .vAlign("middle");

    label.width("100%");
    label.height("100%");
    // устанавливаем метку как контент в центре
    chart.center().content(label);

    // улучшение всплывающей подсказки
    chart.tooltip(true);
//    chart.tooltip().background().fill("#663399");
    chart.tooltip().format("Общая протяженность: {%y} м");

    // установить заливку при выборе
    // chart.selected().fill("#007247");

    // настройка контура при выборе
    // chart
    //     .selected()
    //     .outline()
    //     .fill(function () {
    //         return anychart.color.lighten("#007247", 0.55);
    //     });

    // строим получившуюся диаграмму
    chart.draw();
}


