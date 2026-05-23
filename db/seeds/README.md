# Seeds de base de datos

## Cómo aplicar

⚠️ **Importante:** en Windows PowerShell, `Get-Content ... | docker exec -i ... psql` corrompe los acentos por la conversión cp1252. Usa `docker cp` + `psql -f`:

```powershell
$src = "c:\Users\Patrick Isla\Desktop\notion\MangoVision\db\seeds\diseases.sql"
docker cp $src mangovision-postgres:/tmp/diseases.sql
docker exec mangovision-postgres psql -U mangovision -d mangovision -f /tmp/diseases.sql
```

En Linux/macOS basta con `psql -f db/seeds/diseases.sql` con las variables `PG*` apuntando al contenedor.

## Archivos

- `diseases.sql` — catálogo de 5 enfermedades (EN-021). Idempotente vía `ON CONFLICT DO NOTHING`.
