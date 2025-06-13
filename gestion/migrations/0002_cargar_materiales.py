from django.db import migrations

def cargar_materiales(apps, schema_editor):
    Material = apps.get_model('gestion', 'Material')
    materiales_data = [
        {"nombre": "Papel y cartón", "descripcion": "Incluye cajas, hojas, periódicos, cuadernos (sin espirales ni plásticos)."},
        {"nombre": "Plásticos reciclables", "descripcion": "Botellas PET, envases de alimentos, tapas plásticas. No se aceptan bolsas ni film."},
        {"nombre": "Vidrios", "descripcion": "Botellas y frascos sin tapa. No se reciben vidrios rotos ni espejos."},
        {"nombre": "Latas", "descripcion": "Latas de aluminio y hojalata, como bebidas o conservas."},
        {"nombre": "Electrónicos pequeños", "descripcion": "Celulares, tablets, teclados, cargadores. No se aceptan refrigeradores ni TV."},
        {"nombre": "Textiles", "descripcion": "Ropa en buen estado, sábanas, cortinas. No se aceptan prendas sucias o rotas."},
        {"nombre": "Voluminosos reciclables", "descripcion": "Muebles, colchones, bicicletas, palets."},
    ]
    for data in materiales_data:
        Material.objects.get_or_create(nombre=data['nombre'], defaults=data)

class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(cargar_materiales),
    ]