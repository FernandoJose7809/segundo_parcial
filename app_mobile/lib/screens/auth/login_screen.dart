import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../config/constants.dart';
import '../../routes/app_routes.dart';
import '../../services/api.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({Key? key}) : super(key: key);

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  String _username = '';
  String _password = '';
  bool _isLoading = false;
  String? _errorMessage;

  void _login() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final api = ApiService();
    try {
      final response = await api.post('token/', {
        'username': _username,
        'password': _password,
      });

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final access = data['access'];
        final refresh = data['refresh'];

        // Guardar los tokens
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('access', access);
        await prefs.setString('refresh', refresh);

        // Obtener el ID del estudiante usando el token de acceso
        final userResponse = await api.get(
          'Estudiantes/me/', // Ajusta la ruta según tu API
          headers: {'Authorization': 'Bearer $access'},
        );

        if (userResponse.statusCode == 200) {
          final userData = jsonDecode(userResponse.body);
          final studentId = userData['id'];
          await prefs.setInt('student_id', studentId);
        }

        setState(() {
          _isLoading = false;
        });
        Navigator.pushReplacementNamed(context, AppRoutes.home);
      } else {
        setState(() {
          _isLoading = false;
          _errorMessage = 'Usuario o contraseña incorrectos';
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        _errorMessage = 'Error de conexión. Intente nuevamente.';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: backgroundColor,
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(defaultPadding),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text('Iniciar Sesión', style: headerStyle),
                const SizedBox(height: 32),
                TextFormField(
                  decoration: inputDecoration.copyWith(
                    labelText: 'Usuario',
                    prefixIcon: const Icon(Icons.person_outline),
                  ),
                  style: inputTextStyle,
                  validator: (value) => value == null || value.isEmpty
                      ? 'Ingrese su usuario'
                      : null,
                  onChanged: (value) => _username = value,
                ),
                const SizedBox(height: 16),
                TextFormField(
                  decoration: inputDecoration.copyWith(
                    labelText: 'Contraseña',
                    prefixIcon: const Icon(Icons.lock_outline),
                  ),
                  style: inputTextStyle,
                  obscureText: true,
                  validator: (value) => value == null || value.isEmpty
                      ? 'Ingrese su contraseña'
                      : null,
                  onChanged: (value) => _password = value,
                ),
                const SizedBox(height: 24),
                if (_errorMessage != null)
                  Text(
                    _errorMessage!,
                    style: smallTextStyle.copyWith(color: errorColor),
                  ),
                const SizedBox(height: 8),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    style: elevatedButtonStyle,
                    onPressed: _isLoading
                        ? null
                        : () {
                            if (_formKey.currentState!.validate()) {
                              _login();
                            }
                          },
                    child: _isLoading
                        ? const CircularProgressIndicator(
                            valueColor:
                                AlwaysStoppedAnimation<Color>(Colors.white),
                          )
                        : Text('Ingresar', style: buttonTextStyle),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
