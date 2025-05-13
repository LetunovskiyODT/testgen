<!-- 
# TestGen 
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/LetunovskiyODT/testgen/main/logo.png" alt="TestGen Logo" width="150"/>
  
  <h1>TestGen</h1>
  
  <p>
    <strong>Мощная утилита для генерации тестов для различных языков программирования</strong>
  </p>
  
  <p>
    <a href="https://github.com/LetunovskiyODT/testgen/releases/latest"><img src="https://img.shields.io/github/v/release/LetunovskiyODT/testgen?include_prereleases&style=flat-square&color=blue" alt="Версия"/></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?style=flat-square" alt="Лицензия"/></a>
    <img src="https://img.shields.io/badge/Платформа-Windows-blue?style=flat-square" alt="Платформа"/>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" alt="Python"/>
    <a href="https://github.com/LetunovskiyODT/testgen/actions/workflows/tests.yml"><img src="https://github.com/LetunovskiyODT/testgen/actions/workflows/tests.yml/badge.svg" alt="Tests"/></a>
    <a href="https://github.com/LetunovskiyODT/testgen/actions/workflows/lint.yml"><img src="https://github.com/LetunovskiyODT/testgen/actions/workflows/lint.yml/badge.svg" alt="Lint"/></a>
    <a href="https://codecov.io/gh/LetunovskiyODT/testgen"><img src="https://codecov.io/gh/LetunovskiyODT/testgen/branch/main/graph/badge.svg" alt="Coverage"></a>
  </p>
  
  <h2>Скачать TestGen</h2>
  
  <p>
    <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Portable.zip"><img src="https://img.shields.io/badge/⬇ СКАЧАТЬ-TestGen_Portable-blue?style=for-the-badge" alt="Скачать портативную версию"/></a>
    <br><br>
    <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Full.zip"><img src="https://img.shields.io/badge/⬇ СКАЧАТЬ-TestGen_Full-green?style=for-the-badge" alt="Скачать полную версию"/></a>
    <br><br>
    <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Setup.bat"><img src="https://img.shields.io/badge/⬇ СКАЧАТЬ-TestGen_Setup-red?style=for-the-badge" alt="Скачать установщик"/></a>
  </p>
</div>

<hr>

<details open>
  <summary><strong>📑 Содержание</strong></summary>
  <ol>
    <li><a href="#about">О проекте</a></li>
    <li><a href="#features">Особенности</a></li>
    <li><a href="#installation">Установка</a></li>
    <li><a href="#usage">Использование</a></li>
    <li><a href="#languages">Поддерживаемые языки</a></li>
    <li><a href="#ui">Интерфейс</a></li>
    <li><a href="#development">Для разработчиков</a></li>
    <li><a href="#license">Лицензия</a></li>
  </ol>
</details>

<h2 id="about">📋 О проекте</h2>

<p>
  <strong>TestGen</strong> — это мощная утилита командной строки, предназначенная для автоматизации создания и запуска тестов для различных языков программирования. TestGen анализирует код и создает заготовки тестов на основе обнаруженных функций, классов и методов.
</p>

<p>
  Проект разработан для помощи разработчикам в создании качественных тестов с минимальными усилиями, поддерживает множество языков программирования и фреймворков для тестирования.
</p>

<h2 id="features">✨ Особенности</h2>

<ul>
  <li>🔍 <strong>Интеллектуальный анализ кода</strong> — автоматически находит функции и классы для тестирования</li>
  <li>🌐 <strong>Поддержка множества языков</strong> — Python, JavaScript, TypeScript, Java, C#, Go, Ruby, PHP, Kotlin, Swift и другие</li>
  <li>🧪 <strong>Разнообразные тестовые фреймворки</strong> — pytest, unittest, Jest, Mocha, JUnit, NUnit, testify и другие</li>
  <li>🚀 <strong>Интеграция с CI/CD</strong> — генерация конфигураций для GitHub Actions, GitLab CI, Jenkins</li>
  <li>📊 <strong>Красивый интерфейс консоли</strong> — с использованием Rich для лучшей визуализации</li>
  <li>⚙️ <strong>Настраиваемые шаблоны</strong> — возможность настройки генерируемых тестов</li>
</ul>

<h2 id="installation">⚙️ Установка</h2>

<h3>Установка в Windows</h3>

<div>
  <ol>
    <li>
      <strong>Автоматическая установка (рекомендуется):</strong>
      <ul>
        <li>Скачайте <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Setup.bat">установщик TestGen</a></li>
        <li>Запустите TestGen_Setup.bat от имени администратора</li>
        <li>Следуйте инструкциям установщика</li>
        <li>После установки TestGen будет доступен в меню Пуск, на рабочем столе и через команду <code>testgen</code> в командной строке</li>
      </ul>
    </li>
    <li>
      <strong>Портативная версия:</strong>
      <ul>
        <li>Скачайте <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Portable.zip">архив портативной версии</a></li>
        <li>Распакуйте архив в любую директорию</li>
        <li>Запустите ЗАПУСТИТЬ_TESTGEN.bat или testgen.exe</li>
      </ul>
    </li>
    <li>
      <strong>Полная версия с исходным кодом:</strong>
      <ul>
        <li>Скачайте <a href="https://github.com/LetunovskiyODT/testgen/releases/latest/download/TestGen_Full.zip">архив полной версии</a></li>
        <li>Распакуйте архив в любую директорию</li>
        <li>Используйте исполняемый файл или запустите из исходников с помощью Python</li>
      </ul>
    </li>
  </ol>
</div>

<h3>Установка из исходников (для разработки):</h3>

<pre><code>git clone https://github.com/LetunovskiyODT/testgen.git
cd testgen
pip install -r requirements.txt</code></pre>

<h2 id="usage">📚 Использование</h2>

<p>
  TestGen предоставляет набор команд для работы с тестами:
</p>

<pre><code>testgen init           # Инициализация проекта и создание конфигурации
testgen gen            # Генерация тестов для проекта
testgen run            # Запуск тестов
testgen config         # Настройка проекта и шаблонов
testgen report         # Генерация отчёта с результатами тестирования
testgen ci             # Генерация конфигураций для CI инструментов</code></pre>

<h3>Пример использования:</h3>

<p>Инициализация TestGen в проекте:</p>

<pre><code>$ testgen init --lang python
✓ Инициализирован проект TestGen с поддержкой Python
✓ Создан файл конфигурации testgen.config.json</code></pre>

<p>Генерация тестов для указанного файла:</p>

<pre><code>$ testgen gen --file src/calculator.py
✓ Анализ кода: найдено 5 функций и 2 класса
✓ Генерация тестов: создано 12 тестов в tests/test_calculator.py</code></pre>

<p>Запуск сгенерированных тестов:</p>

<pre><code>$ testgen run
✓ Запуск тестов для Python (pytest)
✓ Пройдено тестов: 10/12
✓ Подробности: 2 теста требуют доработки (см. отчет)</code></pre>

<h2 id="languages">🌐 Поддерживаемые языки и фреймворки</h2>

<div>
  <table>
    <thead>
      <tr>
        <th>Язык</th>
        <th>Фреймворки тестирования</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Python</td>
        <td>pytest, unittest, nose, doctest</td>
      </tr>
      <tr>
        <td>JavaScript</td>
        <td>Jest, Mocha, Jasmine, QUnit</td>
      </tr>
      <tr>
        <td>TypeScript</td>
        <td>Jest, Mocha, Jasmine, AVA</td>
      </tr>
      <tr>
        <td>Java</td>
        <td>JUnit, TestNG, Mockito</td>
      </tr>
      <tr>
        <td>C#</td>
        <td>NUnit, xUnit, MSTest</td>
      </tr>
      <tr>
        <td>Go</td>
        <td>testing, testify, gocheck</td>
      </tr>
      <tr>
        <td>Ruby</td>
        <td>RSpec, Minitest, Cucumber</td>
      </tr>
      <tr>
        <td>PHP</td>
        <td>PHPUnit, Codeception, Pest</td>
      </tr>
      <tr>
        <td>Kotlin</td>
        <td>JUnit, KotlinTest, Spek</td>
      </tr>
      <tr>
        <td>Swift</td>
        <td>XCTest, Quick, Nimble</td>
      </tr>
      <tr>
        <td>Rust</td>
        <td>cargo test, mockiato</td>
      </tr>
      <tr>
        <td>C/C++</td>
        <td>Google Test, Catch2, Boost.Test</td>
      </tr>
      <tr>
        <td>Perl</td>
        <td>Test::More, Test::Unit</td>
      </tr>
      <tr>
        <td>Haskell</td>
        <td>HUnit, QuickCheck</td>
      </tr>
      <tr>
        <td>Scala</td>
        <td>ScalaTest, Specs2</td>
      </tr>
    </tbody>
  </table>
</div>

<h2 id="ui">🖥️ Интерфейс</h2>

<p>
  TestGen использует библиотеку <strong>rich</strong> для создания красивого и интуитивно понятного интерфейса командной строки, который включает:
</p>

<ul>
  <li>Цветную подсветку кода</li>
  <li>Интерактивные меню выбора</li>
  <li>Прогресс-бары для длительных операций</li>
  <li>Красивые таблицы для представления результатов</li>
  <li>Древовидные структуры для отображения найденных функций и классов</li>
</ul>

<div align="center">
  <p><em>Скриншоты интерфейса будут добавлены позже</em></p>
</div>

<h2 id="development">👨‍💻 Для разработчиков</h2>

<h3>Структура проекта</h3>

<pre><code>testgen/
├── cmd/             # Директория для команд CLI
├── ui/              # Компоненты для интерфейса (rich)
├── langs/           # Генераторы тестов для разных языков
├── testengines/     # Запуск тестов, анализ результатов
├── ci/              # Интеграции с CI/CD инструментами
├── tests/           # Тесты для самого TestGen
└── README.md        # Документация</code></pre>

<h3>Запуск тестов</h3>

<pre><code>pytest tests/</code></pre>

<h3>Сборка проекта</h3>

<pre><code>python installer.py</code></pre>

<h2 id="license">📄 Лицензия</h2>

<p>
  Этот проект лицензирован под <a href="LICENSE">Apache License 2.0</a> — см. файл LICENSE для деталей.
</p>

<hr>

<div align="center">
  <p>Сделано с ❤️ командой TestGen</p>
  <p>
    <a href="https://github.com/LetunovskiyODT/testgen/issues">Сообщить о проблеме</a> · 
    <a href="https://github.com/LetunovskiyODT/testgen/discussions">Обсуждения</a> · 
    <a href="https://github.com/LetunovskiyODT/testgen/wiki">Вики</a>
  </p>
</div>

## Скачать

[![Скачать последнюю версию](https://img.shields.io/github/v/release/LetunovskiyODT/testgen)](https://github.com/LetunovskiyODT/testgen/releases/latest)
 