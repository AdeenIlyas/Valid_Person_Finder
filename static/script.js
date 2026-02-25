document.addEventListener('DOMContentLoaded', function() {
    const singleSearchForm = document.getElementById('single-search-form');
    const batchSearchForm = document.getElementById('batch-search-form');
    const loader = document.getElementById('loader');
    const singleResultContainer = document.getElementById('single-result');
    const batchResultsTable = document.getElementById('batch-results-table');
    const batchResultsBody = batchResultsTable.querySelector('tbody');

    singleSearchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const company = document.getElementById('company').value;
        const designation = document.getElementById('designation').value;

        showLoader(true);
        clearResults();

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ company, designation })
        })
        .then(response => response.json())
        .then(data => {
            showLoader(false);
            if (data.error) {
                singleResultContainer.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                singleResultContainer.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
        })
        .catch(error => {
            showLoader(false);
            singleResultContainer.innerHTML = `<p>Error: ${error.toString()}</p>`;
        });
    });

    batchSearchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        showLoader(true);
        clearResults();

        fetch('/batch', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            showLoader(false);
            batchResultsTable.classList.remove('hidden');
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${row['Title']}</td>
                    <td>${row['Company Name']}</td>
                    <td>${row['First Name']}</td>
                    <td>${row['Last Name']}</td>
                    <td>${row['Source']}</td>
                `;
                batchResultsBody.appendChild(tr);
            });
        })
        .catch(error => {
            showLoader(false);
            singleResultContainer.innerHTML = `<p>Error: ${error.toString()}</p>`;
        });
    });

    function showLoader(show) {
        if (show) {
            loader.classList.remove('hidden');
        } else {
            loader.classList.add('hidden');
        }
    }

    function clearResults() {
        singleResultContainer.innerHTML = '';
        batchResultsBody.innerHTML = '';
        batchResultsTable.classList.add('hidden');
    }
});