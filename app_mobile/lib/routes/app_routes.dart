import 'package:flutter/material.dart';
import '../screens/auth/login_screen.dart';
import '../screens/dashboard/home_screen.dart';
import '../screens/notas/notas_screen.dart';
import '../screens/perfil/perfil_screen.dart';

class AppRoutes {
  static const login = '/login';
  static const home = '/home';
  static const materias = '/materias';
  static const notas = '/notas';
  static const perfil = '/perfil';

  static Map<String, WidgetBuilder> get routes => {
        login: (_) => const LoginScreen(),
        home: (_) => const HomeScreen(),
        perfil: (_) => const PerfilScreen(),
      };
}
