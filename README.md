Harvard-CS50x---Final-Project-Intelligent-Income-Tax-Calculator-
The "Intelligent Income Tax Calculator" is an innovative web application that offers users a modern and user-friendly platform to calculate their annual income tax and Income Tax Withheld at Source (IRRF) #Title: Intelligent Income Tax Calculator

Video Demo: https://youtu.be/YeTv6mRLgmU
Description: The "Intelligent Income Tax Calculator" is an innovative web application that offers users a modern and user-friendly platform to calculate their annual income tax and Income Tax Withheld at Source (IRRF). With a sleek and intuitive design, the application provides accurate tax calculations based on the user's input of annual salary, deductions, and IRRF. It employs advanced algorithms to ensure precise tax estimations and incorporates a unique feature to determine the optimal choice between tax reimbursement and simplified deductions. This application not only simplifies the complex tax calculation process but also enhances financial planning and decision-making for users.
https://github.com/gugs881/Harvard-CS50x---Final-Project-Intelligent-Income-Tax-Calculator-/edit/main/README.md












<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Calculadora de Imposto de Renda</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f1f1f1;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }

    .container {
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      padding: 20px;
      max-width: 400px;
      text-align: center;
    }

    h1 {
      color: #333;
      margin-bottom: 20px;
    }

    label {
      display: block;
      margin-bottom: 5px;
      color: #666;
      font-weight: bold;
    }

    input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 4px;
      margin-bottom: 15px;
    }

    button {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 10px 20px;
      border-radius: 4px;
      cursor: pointer;
      width: 100%;
      transition: background-color 0.3s ease;
    }

    button:hover {
      background-color: #0056b3;
    }

    .resultado {
      display: block;
      margin-top: 15px;
      padding: 10px;
      background-color: #007bff;
      color: white;
      border-radius: 4px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Calculadora de Imposto de Renda</h1>
    <label for="salario">Salário Anual:</label>
    <input type="number" id="salario" placeholder="Informe o salário anual">
    <label for="deducoes">Deduções:</label>
    <input type="number" id="deducoes" placeholder="Informe as deduções">
    <label for="irrf">Imposto de Renda Retido na Fonte:</label>
    <input type="number" id="irrf" placeholder="Informe o IRRF">
    <button onclick="calcularImpostoERestituicao()">Calcular Imposto</button>
    <p>Total de Imposto de Renda: <span class="resultado" id="resultadoImposto">R$ 0.00</span></p>
    <p>Restituição de Imposto: <span class="resultado" id="restituicaoImposto">R$ 0.00</span></p>
  </div>
  <script>
    function calcularImpostoERestituicao() {
      const salarioAnual = parseFloat(document.getElementById('salario').value);
      const deducoes = parseFloat(document.getElementById('deducoes').value);
      const irrf = parseFloat(document.getElementById('irrf').value);
      const resultadoImpostoElement = document.getElementById('resultadoImposto');
      const restituicaoImpostoElement = document.getElementById('restituicaoImposto');

      if (!isNaN(salarioAnual) && !isNaN(deducoes) && !isNaN(irrf)) {
        const baseCalculo = salarioAnual - deducoes;
        let imposto = 0;
        let restituicao = 0;

        if (baseCalculo <= 22000) {
          imposto = baseCalculo * 0.075 - irrf;
        } else if (baseCalculo <= 33000) {
          imposto = baseCalculo * 0.15 - irrf;
        } else if (baseCalculo <= 44000) {
          imposto = baseCalculo * 0.225 - irrf;
        } else {
          imposto = baseCalculo * 0.275 - irrf;
        }

        if (baseCalculo * 0.2 <= 16734.26) {
          restituicao = baseCalculo * 0.2;
        } else {
          restituicao = 16734.26;
        }

        resultadoImpostoElement.textContent = `R$ ${imposto.toFixed(2)}`;
        restituicaoImpostoElement.textContent = `R$ ${restituicao.toFixed(2)}`;
      } else {
        resultadoImpostoElement.textContent = 'Informe valores válidos';
        restituicaoImpostoElement.textContent = '';
      }
    }
  </script>
</body>
</html>
