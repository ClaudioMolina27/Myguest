/* ============================================================
   SCRIPT 00 - SCRIPT MAESTRO
   Ejecuta todos los scripts en el orden correcto.

   Uso desde psql:
     psql -U <usuario> -d <base_de_datos> -f "00 - Script maestro.sql"

   O ejecutar cada script individualmente en este orden:
     01 → DDL (esquema y FK)
     02 → Parámetros del sistema
     03 → Usuarios
     04 → Talleres
     05 → Productos
     06 → Config taller (relación taller-producto)
     07 → Programación de asignaturas
     08 → Programación de talleres
     09 → Registros de ejecución de talleres
     10 → Detalle de registros (generado desde 09 + 06)
   ============================================================ */

\i '01 - Script creacion esquema.sql'
\i '02 - Carga tablas de parametros.sql'
\i '03 - Carga usuario.sql'
\i '04 - Carga taller.sql'
\i '05 - Carga producto.sql'
\i '06 - Carga config_taller.sql'
\i '07 - Carga prog_asign.sql'
\i '08 - Carga prog_taller.sql'
\i '09 - Carga regis_taller.sql'
\i '10 - Carga det_regis_taller.sql'
