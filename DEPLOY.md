# 🚀 Cómo Subir a GitHub

## Opción 1: GitHub CLI (Recomendada)

```bash
# Desde el directorio siendo-apps
gh auth login
gh repo create sendo-apps --public --source=. --push
```

## Opción 2: Crear manualmente en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: **sendo-apps**
3. Descripción: **Apps familiares SER SENDO - Planificador comidas + ejercicio + web premium**
4. Público ✅
5. NO inicializar con README (ya lo tenemos)
6. Click "Create repository"

Luego ejecuta:
```bash
git remote add origin https://github.com/TU_USUARIO/sendo-apps.git
git branch -M main
git push -u origin main
```

## 🌐 GitHub Pages (Hosting gratuito)

1. En el repo, ve a **Settings** > **Pages**
2. Source: **Deploy from a branch**
3. Branch: **main** / **/ (root)**
4. Save

Tu app estará disponible en:
**https://TU_USUARIO.github.io/sendo-apps/**

## 📱 URLs Directas

- **Comidas**: https://TU_USUARIO.github.io/sendo-apps/
- **Ejercicio**: https://TU_USUARIO.github.io/sendo-apps/ejercicio.html
- **Web SENDO**: https://TU_USUARIO.github.io/sendo-apps/sendo.html
- **Launcher**: https://TU_USUARIO.github.io/sendo-apps/launcher.html

## 🔄 Para actualizar

```bash
git add .
git commit -m "📱 Actualización apps"
git push
```

¡Listo! Las apps estarán disponibles online 24/7.