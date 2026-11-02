import socket
import json
import time

HOST = "localhost"
PORT_R = 9000
PORT_F = 9001

weather = {
    "city": "Москва",
    "temp": -5,
    "humidity": 80,
    "is_snowing": True
}


def send_reliable(message):
    """Отправляет сообщение по TCP и возвращает ответ и время."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT_R))
        start = time.perf_counter()
        client.sendall(json.dumps(message, ensure_ascii=False).encode("utf-8"))
        response = client.recv(4096)
        elapsed = time.perf_counter() - start
        return json.loads(response.decode("utf-8")), elapsed
    finally:
        client.close()


def send_fast(message):
    """Отправляет сообщение по UDP и возвращает ответ и время."""
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2.0)
    start = time.perf_counter()
    try:
        client.sendto(
            json.dumps(message, ensure_ascii=False).encode("utf-8"),
            (HOST, PORT_F)
        )
        response, _ = client.recvfrom(4096)
        elapsed = time.perf_counter() - start
        return json.loads(response.decode("utf-8")), elapsed
    except socket.timeout:
        return {"status": "TIMEOUT"}, time.perf_counter() - start
    finally:
        client.close()


if __name__ == "__main__":
    print("=== Отправка через TCP ===")
    try:
        response, elapsed = send_reliable(weather)
        print(f"Ответ: {response}")
        print(f"Время: {elapsed * 1000:.2f} мс")
    except OSError as error:
        print(f"Ошибка TCP: {error}")

    print("\n=== Отправка через UDP ===")
    response, elapsed = send_fast(weather)
    print(f"Ответ: {response}")
    print(f"Время: {elapsed * 1000:.2f} мс")
