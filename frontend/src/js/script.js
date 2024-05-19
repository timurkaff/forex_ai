document.addEventListener('DOMContentLoaded', function() {
    // Находим все кнопки с тикерами
    const tickerButtons = document.querySelectorAll('[data-ticker]');
    // Находим элементы для отображения данных
    const currentTickerElement = document.getElementById('current_ticker');
    const currentPriceElement = document.getElementById('current_price');
    const futurePriceElement = document.getElementById('future_price');
    const currencyElement = document.getElementById('currency');
    const blockPriceElement = document.getElementById('block_price');

    function comparePrices(currentPrice, forecastedPrice) {
        return forecastedPrice > currentPrice? 'green' : 'red';
    }

    function fetchData(ticker) {
        fetch(`http://127.0.0.1:8000/predict/${ticker}`)
      .then(response => response.json())
      .then(data => {
            currentTickerElement.textContent = ticker;
            currentPriceElement.textContent = `${data['Current Close Price']}`;
            futurePriceElement.textContent = `${data['Forecasted Next Close Price']}`;

            const priceComparisonColor = comparePrices(data['Current Close Price'], data['Forecasted Next Close Price']);

            futurePriceElement.style.color = priceComparisonColor;

            currencyElement.classList.add('hidden');
            blockPriceElement.classList.remove('hidden');
        })
      .catch(error => console.error('Error fetching data:', error));
    }

    tickerButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const ticker = event.target.getAttribute('data-ticker');
            fetchData(ticker);
        });
    });
});