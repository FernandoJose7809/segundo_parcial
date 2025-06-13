import 'package:flutter/material.dart';
import '../../config/constants.dart';
import '../../widgets/drawer_widget.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../services/api.dart';
import 'dart:convert';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String? nombreEstudiante;
  List<dynamic> materias = [];
  bool isLoading = true;
  String? error;
  int? materiaSeleccionada; // Para controlar la expansión

  // Nueva variable para almacenar predicciones y consejos
  Map<int, Map<String, dynamic>> predicciones =
      {}; // degreeSubjectId -> {prediccion, consejo}

  @override
  void initState() {
    super.initState();
    cargarDatos();
  }

  Future<void> cargarDatos() async {
    final prefs = await SharedPreferences.getInstance();
    final studentId = prefs.getInt('student_id');
    final access = prefs.getString('access');
    if (studentId == null || access == null) {
      setState(() {
        nombreEstudiante = '';
        isLoading = false;
        error = 'No se encontró información del estudiante.';
      });
      return;
    }
    final api = ApiService();

    // Obtener nombre del estudiante
    final response = await api.get(
      'Estudiantes/$studentId/',
      headers: {'Authorization': 'Bearer $access'},
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      nombreEstudiante = data['first_name'] ?? '';
    } else {
      nombreEstudiante = '';
    }

    // Obtener curso del estudiante
    final cursoResp = await api.get(
      'CursoPorEstudiante/?student=$studentId',
      headers: {'Authorization': 'Bearer $access'},
    );
    if (cursoResp.statusCode != 200) {
      setState(() {
        error = 'No se pudo obtener el curso del estudiante.';
        isLoading = false;
      });
      return;
    }
    final cursos = jsonDecode(cursoResp.body);
    if (cursos.isEmpty) {
      setState(() {
        error = 'El estudiante no tiene curso asignado.';
        isLoading = false;
      });
      return;
    }
    final gradeId = cursos[0]['grade'];

    // Obtener materias del grado
    final materiasResp = await api.get(
      'MateriaPorCurso/?grade=$gradeId',
      headers: {'Authorization': 'Bearer $access'},
    );
    if (materiasResp.statusCode != 200) {
      setState(() {
        error = 'No se pudieron obtener las materias.';
        isLoading = false;
      });
      return;
    }
    final materiasData = jsonDecode(materiasResp.body);

    // Obtener notas del estudiante
    final notasResp = await api.get(
      'Notas/?student=$studentId',
      headers: {'Authorization': 'Bearer $access'},
    );
    List<dynamic> notasData = [];
    if (notasResp.statusCode == 200) {
      notasData = jsonDecode(notasResp.body);
    }

    setState(() {
      materias = materiasData.map((materia) {
        final nota = notasData.firstWhere(
          (n) => n['degreeSubject'] == materia['id'],
          orElse: () => null,
        );
        return {
          ...materia,
          'nota': nota != null ? nota['note'] : null,
        };
      }).toList();
      isLoading = false;
    });
  }

  Future<void> obtenerPrediccion(int degreeSubjectId, String access) async {
    final api = ApiService();
    final response = await api.post(
      'prediccion/',
      {'degreeSubject': degreeSubjectId},
      headers: {'Authorization': 'Bearer $access'},
    );
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        predicciones[degreeSubjectId] = data;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        backgroundColor: primaryColor,
      ),
      drawer: const DrawerWidget(),
      backgroundColor: backgroundColor,
      body: Padding(
        padding: const EdgeInsets.all(defaultPadding),
        child: isLoading
            ? const Center(child: CircularProgressIndicator())
            : error != null
                ? Center(child: Text(error!, style: labelStyle))
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Bienvenido${nombreEstudiante != null && nombreEstudiante!.isNotEmpty ? ', $nombreEstudiante' : ''}',
                        style: headerStyle,
                      ),
                      const SizedBox(height: 20),
                      Text(
                        'Materias inscritas:',
                        style: labelStyle.copyWith(fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Expanded(
                        child: materias.isEmpty
                            ? const Text('No hay materias inscritas.',
                                style: labelStyle)
                            : ListView.builder(
                                itemCount: materias.length,
                                itemBuilder: (context, index) {
                                  final materia = materias[index];
                                  final isOpen = materiaSeleccionada == index;
                                  return AnimatedContainer(
                                    duration: const Duration(milliseconds: 200),
                                    margin:
                                        const EdgeInsets.symmetric(vertical: 8),
                                    decoration: BoxDecoration(
                                      color: Colors.white,
                                      borderRadius:
                                          BorderRadius.circular(borderRadius),
                                      boxShadow: [
                                        BoxShadow(
                                          color: Colors.black12,
                                          blurRadius: 6,
                                          offset: Offset(0, 2),
                                        ),
                                      ],
                                      border: Border.all(
                                        color: isOpen
                                            ? accentColor
                                            : primaryColor.withOpacity(0.2),
                                        width: isOpen ? 2 : 1,
                                      ),
                                    ),
                                    child: InkWell(
                                      borderRadius:
                                          BorderRadius.circular(borderRadius),
                                      onTap: () {
                                        setState(() {
                                          materiaSeleccionada =
                                              isOpen ? null : index;
                                        });
                                      },
                                      child: Padding(
                                        padding: const EdgeInsets.symmetric(
                                            horizontal: 16, vertical: 18),
                                        child: Column(
                                          crossAxisAlignment:
                                              CrossAxisAlignment.start,
                                          children: [
                                            Row(
                                              children: [
                                                Icon(Icons.book,
                                                    color: primaryColor),
                                                const SizedBox(width: 12),
                                                Expanded(
                                                  child: Text(
                                                    '${materia['subject_name'] ?? 'Materia'}',
                                                    style: labelStyle.copyWith(
                                                      fontWeight:
                                                          FontWeight.w600,
                                                      fontSize: 18,
                                                      color: Colors.black87,
                                                    ),
                                                  ),
                                                ),
                                                Icon(
                                                  isOpen
                                                      ? Icons.keyboard_arrow_up
                                                      : Icons
                                                          .keyboard_arrow_down,
                                                  color: accentColor,
                                                ),
                                              ],
                                            ),
                                            if (isOpen) ...[
                                              const SizedBox(height: 12),
                                              Divider(
                                                  color: primaryColor
                                                      .withOpacity(0.2)),
                                              Text(
                                                materia['nota'] != null
                                                    ? 'Nota: ${materia['nota'].toStringAsFixed(2)}'
                                                    : 'Sin nota',
                                                style: labelStyle.copyWith(
                                                    color: primaryColor,
                                                    fontWeight:
                                                        FontWeight.bold),
                                              ),
                                              const SizedBox(height: 8),
                                              ElevatedButton(
                                                onPressed: () async {
                                                  final prefs =
                                                      await SharedPreferences
                                                          .getInstance();
                                                  final access =
                                                      prefs.getString(
                                                              'access') ??
                                                          '';
                                                  await obtenerPrediccion(
                                                      materia['id'], access);
                                                },
                                                child: const Text(
                                                    'Ver predicción'),
                                              ),
                                              if (predicciones[materia['id']] !=
                                                  null) ...[
                                                Text(
                                                    'Predicción: ${predicciones[materia['id']]!['prediccion']}'),
                                                Text(
                                                    'Consejo: ${predicciones[materia['id']]!['consejo']}'),
                                              ],
                                            ],
                                          ],
                                        ),
                                      ),
                                    ),
                                  );
                                },
                              ),
                      ),
                    ],
                  ),
      ),
    );
  }
}
