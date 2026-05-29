# Отчет по лабораторной работе 5

Веб-приложение. Обработка GET и POST запросов

## Описание проекта

Написан на языке Go. Для создания веб-сервера использован пакет `net/http` из стандартной библиотеки языка. Тестирование проводится при помощи утилиты `cURL`.  
Выбор языка обусловлен отсутствием необходимости подключения отдельных фреймворков для создания HTTP-сервера. Также синтаксис позволяет писать понятный и краткий код.

## Структура проекта

```
l5/
├── main.go        # Основной файл приложения
├── go.mod         # Файл конфигурации
├── go.sum         # Контрольные суммы
└── README.md      # Отчет
```

## Код проекта
```go
// main.go

package main

import (
	"encoding/json"
	"log"

	"net/http"

	"github.com/google/uuid"
)

type Response struct {
	Message string `json:"message"`
}

type ReverseRequest struct {
	Text string `json:"text"`
}

type ReverseResponse struct {
	Reversed string `json:"reversed"`
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("Hello, this is 1155281"))
}

func idHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	id := uuid.New().String()
	response := map[string]string{"id": id}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func reverseHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req ReverseRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	reversed := reverseString(req.Text)

	response := ReverseResponse{Reversed: reversed}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func pingHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte("pong"))
}

func reverseString(s string) string {
	chars := []rune(s)
	for i, j := 0, len(chars)-1; i < j; i, j = i+1, j-1 {
		chars[i], chars[j] = chars[j], chars[i]
	}
	return string(chars)
}

func main() {
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/id", idHandler)
	http.HandleFunc("/reverse", reverseHandler)
	http.HandleFunc("/ping", pingHandler)

	log.Println("Server starting on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
```

## API

### GET `/` - домашняя страница

Возвращает приветственную строку с логином в Moodle.

**Ответ:**
```
Hello, this is 1155281
```

### GET `/id` - получить UUID

Генерирует и возвращает уникальный UUID.
Используется пакет google/uuid.

**Ответ:**
```json
{
  "id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"
}
```

### POST `/reverse` - вернуть строку в обратном порядке

Принимает JSON с полем `text` и возвращает перевёрнутую строку.

**Запрос:**
```json
{
  "text": "hello"
}
```

**Ответ:**
```json
{
  "reversed": "olleh"
}
```

### GET `/ping`

Проверяет доступность сервиса.

**Ответ:**
```
pong
```

## Инструкция по запуску

1. Убедитесь, что установлен Go (версия 1.16 или выше)
2. Инициализируйте модуль (если нужно): `go mod init webapp`
3. Загрузите зависимости: `go mod tidy`
4. Запустите приложение: `go run main.go`
5. Сервис будет доступен на http://localhost:8080/

## Тестирование с cURL

### Запрос `GET http://localhost:8080/`
```ps
curl -X GET http://localhost:8080/
Hello, this is 1155281
```

### Запрос `GET http://localhost:8080/id`
```ps
 curl -X GET http://localhost:8080/id
{"id":"f699c54d-d59c-4443-ad0a-6b1c6c59edf0"}

curl -X GET http://localhost:8080/id
{"id":"e4f6e906-4b03-488e-9dbb-eb9799064ce2"}
```
Убеждаемся в том, что каждый запрос вернёт уникальный случайный UUID.

### Запрос `POST http://localhost:8080/reverse`
```ps
curl -X POST http://localhost:8080/reverse \
 -H "Content-Type: application/json" \
 -d '{"text":"hello"}'

{"reversed":"olleh"}
```

### Запрос `GET http://localhost:8080/ping`
```ps
curl -X GET http://localhost:8080/ping
pong
```
