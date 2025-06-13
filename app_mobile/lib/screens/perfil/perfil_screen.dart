import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../services/api.dart';
import 'dart:convert';

class PerfilScreen extends StatefulWidget {
  const PerfilScreen({Key? key}) : super(key: key);

  @override
  State<PerfilScreen> createState() => _PerfilScreenState();
}

class _PerfilScreenState extends State<PerfilScreen> {
  Map<String, dynamic>? estudiante;
  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    cargarPerfil();
  }

  Future<void> cargarPerfil() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final studentId = prefs.getInt('student_id');
      final access = prefs.getString('access');
      if (studentId == null || access == null) {
        setState(() {
          error = 'No se encontró información del estudiante.';
          isLoading = false;
        });
        return;
      }

      final api = ApiService();
      final response = await api.get(
        'Estudiantes/$studentId/',
        headers: {'Authorization': 'Bearer $access'},
      );

      if (response.statusCode == 200) {
        setState(() {
          estudiante = jsonDecode(response.body);
          isLoading = false;
        });
      } else {
        setState(() {
          error = 'No se pudo cargar el perfil.';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = 'Error de conexión.';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }
    if (error != null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Perfil')),
        body: Center(child: Text(error!)),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Perfil del Estudiante')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Nombre: ${estudiante?['first_name'] ?? ''}',
                style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 12),
            Text('Apellido: ${estudiante?['last_name'] ?? ''}',
                style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 12),
            Text('Dirección: ${estudiante?['address'] ?? ''}',
                style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 12),
            Text('Teléfono: ${estudiante?['student_phone'] ?? ''}',
                style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 12),
            Text('Correo electrónico: ${estudiante?['student_email'] ?? ''}',
                style: const TextStyle(fontSize: 18)),
          ],
        ),
      ),
    );
  }
}
