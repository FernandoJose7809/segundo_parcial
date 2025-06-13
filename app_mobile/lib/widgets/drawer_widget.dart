import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../routes/app_routes.dart';
import '../services/api.dart';
import 'dart:convert';

class DrawerWidget extends StatefulWidget {
  const DrawerWidget({super.key});

  @override
  State<DrawerWidget> createState() => _DrawerWidgetState();
}

class _DrawerWidgetState extends State<DrawerWidget> {
  bool logueado = false;
  bool cargandoPerfil = true;
  Map<String, dynamic>? perfil;

  @override
  void initState() {
    super.initState();
    cargarPerfil();
  }

  Future<void> cargarPerfil() async {
    final prefs = await SharedPreferences.getInstance();
    final isLogged = prefs.getString('access') != null;
    final studentId = prefs.getInt('student_id');
    final access = prefs.getString('access');

    if (isLogged && studentId != null && access != null) {
      final api = ApiService();
      final response = await api.get(
        'Estudiantes/$studentId/',
        headers: {'Authorization': 'Bearer $access'},
      );
      if (response.statusCode == 200) {
        setState(() {
          perfil = jsonDecode(response.body);
          logueado = true;
          cargandoPerfil = false;
        });
        return;
      }
    }
    setState(() {
      logueado = false;
      cargandoPerfil = false;
      perfil = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    final widthScreen = MediaQuery.of(context).size.width;

    return Drawer(
      child: Column(
        children: [
          Container(
            color: Colors.grey[100],
            padding: EdgeInsets.symmetric(
              horizontal: widthScreen * 0.04,
              vertical: widthScreen * 0.08,
            ),
            width: double.infinity,
            child: cargandoPerfil
                ? const Center(
                    child: CircularProgressIndicator(),
                  )
                : perfil != null
                    ? Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.person_outline,
                                  size: 40, color: Colors.indigo),
                              SizedBox(width: widthScreen * 0.03),
                              Expanded(
                                child: Text(
                                  '${perfil?['first_name'] ?? ''} ${perfil?['last_name'] ?? ''}',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18,
                                    color: Colors.black87,
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 12),
                          Text('Dirección: ${perfil?['address'] ?? ''}',
                              style: const TextStyle(fontSize: 15)),
                          const SizedBox(height: 6),
                          Text('Teléfono: ${perfil?['student_phone'] ?? ''}',
                              style: const TextStyle(fontSize: 15)),
                          const SizedBox(height: 6),
                          Text('Correo: ${perfil?['student_email'] ?? ''}',
                              style: const TextStyle(fontSize: 15)),
                        ],
                      )
                    : const Text(
                        'No se pudo cargar el perfil',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                          color: Colors.redAccent,
                        ),
                      ),
          ),
          const Spacer(),
          const Divider(),
          Padding(
            padding: EdgeInsets.symmetric(
              horizontal: widthScreen * 0.04,
              vertical: widthScreen * 0.02,
            ),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.circular(12),
              ),
              child: ListTile(
                leading: const Icon(Icons.exit_to_app, color: Colors.red),
                title: const Text(
                  'Cerrar sesión',
                  style:
                      TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
                ),
                onTap: () async {
                  final prefs = await SharedPreferences.getInstance();
                  await prefs.remove('access');
                  await prefs.remove('refresh');
                  await prefs.remove('user_name');
                  await prefs.remove('student_id');

                  if (!context.mounted) return;

                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Sesión cerrada correctamente'),
                      backgroundColor: Colors.indigo,
                    ),
                  );

                  Navigator.pushReplacementNamed(context, AppRoutes.login);
                },
              ),
            ),
          ),
        ],
      ),
    );
  }
}
