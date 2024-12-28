document.getElementById('select-service-button').addEventListener('click', function() {
    const selectedService = document.getElementById('service_type').value;
    document.getElementById('form-container').style.display = 'block';
    document.querySelectorAll('.service-form').forEach(form => form.style.display = 'none');

    if (selectedService === 'create_account') {
        document.getElementById('create-account-form').style.display = 'block';
    } else if (selectedService === 'deposit') {
        document.getElementById('deposit-container').style.display = 'block';
    } else if (selectedService === 'withdraw') {
        document.getElementById('withdraw-container').style.display = 'block';
    } else if (selectedService === 'delete_account') {
        document.getElementById('delete-container').style.display = 'block';
 } else if (selectedService === 'check_balance') {
        document.getElementById('balance-inquiry').style.display = 'block';
    }
});

document.getElementById('create-account-button').addEventListener('click', function() {
    const accountData = {
        account_number: document.getElementById('account_number').value,
        account_type: document.getElementById('account_type').value,
        customer_name: document.getElementById('customer_name').value,
        customer_phone: document.getElementById('customer_phone').value,
        customer_age: document.getElementById('customer_age').value,
        customer_address: document.getElementById('customer_address').value
    };

    fetch('/create_account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(accountData)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('deposit-button').addEventListener('click', function() {
    const depositData = {
        account_number: document.getElementById('deposit_account_number').value,
        amount: document.getElementById('deposit_amount').value
    };

    fetch('/deposit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(depositData)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('withdraw-button').addEventListener('click', function() {
    const withdrawData = {
        account_number: document.getElementById('withdraw_account_number').value,
        amount: document.getElementById('withdraw_amount').value
    };

    fetch('/withdraw', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(withdrawData)
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('delete-button').addEventListener('click', function() {
    const accountNumber = document.getElementById('delete_account_number').value;

    fetch(`/delete_account/${accountNumber}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => alert(data.message))
    .catch(error => console.error('Error:', error));
});

document.getElementById('inquiry-button').addEventListener('click', function() {
    const accountNumber = document.getElementById('inquiry_account_number').value;

    fetch(`/check_balance/${accountNumber}`)
    .then(response => response.json())
    .then(data => {
        if (data.balance !== undefined) {
            document.getElementById('balance-result').innerText = `Balance: $${data.balance}`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.querySelectorAll('#back-to-menu-button').forEach(button => {
    button.addEventListener('click', function() {
        document.getElementById('form-container').style.display = 'none';
        document.getElementById('service-selection').style.display = 'block';
    });
});