from django.http import HttpResponse

from homepage.views import page
from storage import load_meters, load_readings


def readings_list(request):
    """Страница со списком всех показаний."""
    meters = load_meters("data/meters.json")
    readings = load_readings("data/readings.json", meters)

    items = ""
    for r in readings:
        items += f"""
        <tr>
            <td>{r.reading_date}</td>
            <td>{r.meter.name}</td>
            <td>{r.previous} → {r.current}</td>
            <td>{r.consumption} {r.meter.unit}</td>
            <td>{r.cost:.2f} руб.</td>
        </tr>
        """

    content = f"""
    <h1>История показаний</h1>
    <table class="table table-striped mt-4">
        <thead>
            <tr>
                <th>Дата</th>
                <th>Счетчик</th>
                <th>Показания</th>
                <th>Расход</th>
                <th>Стоимость</th>
            </tr>
        </thead>
        <tbody>{items}</tbody>
    </table>
    """
    return HttpResponse(page("Показания", content))
