import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../routes/app_routes.dart';

class DrawerWidget extends StatefulWidget {
  const DrawerWidget({super.key});

  @override
  State<DrawerWidget> createState() => _DrawerWidgetState();
}

class _DrawerWidgetState extends State<DrawerWidget> {
  bool logueado = false;
  String nombreUsuario = '';
  bool cargandoNombre = true;

  @override
  void initState() {
    super.initState();
    verificarLogin();
  }

  Future<void> verificarLogin() async {
    final prefs = await SharedPreferences.getInstance();
    final isLogged = prefs.getString('access') != null;
    final cachedName = prefs.getString('user_name');

    setState(() {
      logueado = isLogged;
      nombreUsuario = cachedName ?? '';
      cargandoNombre = false;
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
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Icon(Icons.person_outline,
                    size: 40, color: Colors.indigo),
                SizedBox(width: widthScreen * 0.03),
                Expanded(
                  child: cargandoNombre
                      ? const Text(
                          'Cargando...',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Colors.black45,
                          ),
                        )
                      : Text(
                          logueado ? nombreUsuario : 'Bienvenido',
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
          ),
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                if (logueado) ...[
                  ListTile(
                    leading: const Icon(Icons.person),
                    title: const Text('Perfil'),
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.perfil);
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.book),
                    title: const Text('Materias'),
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.materias);
                    },
                  ),
                  ListTile(
                    leading: const Icon(Icons.grade),
                    title: const Text('Notas'),
                    onTap: () {
                      Navigator.pushNamed(context, AppRoutes.notas);
                    },
                  ),
                ],
                ListTile(
                  leading: const Icon(Icons.settings),
                  title: const Text('Configuración'),
                  onTap: () {
                    Navigator.pop(context);
                  },
                ),
              ],
            ),
          ),
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
