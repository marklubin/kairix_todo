# Kairix Todo Android App

An Android client application for the Kairix Todo web service. This app allows users to manage their tasks with features like voice input, bulk entry, and clipboard integration.

## Features

- Create, edit, delete, and complete tasks
- View tasks by different timeframes (Today, Tomorrow, This Week)
- Tag tasks for organization
- Voice input for hands-free task creation
- Bulk entry for quickly adding multiple tasks
- Copy tasks to clipboard as a formatted list
- Offline support with background synchronization
- Reminder notifications

## Project Structure

```
android/
├── app/                  # Application module
├── docs/                 # Documentation
│   ├── ui_mockups.md     # UI mockups and design specs
│   ├── user_stories.md   # User stories and acceptance criteria
│   └── system_design.md  # System architecture and technical design
└── README.md             # Project overview (this file)
```

## Documentation

- [UI Mockups](docs/ui_mockups.md) - Visual design and UI components
- [User Stories](docs/user_stories.md) - Functional requirements as user stories
- [System Design](docs/system_design.md) - Technical architecture and implementation details

## Getting Started

### Prerequisites

- Android Studio Arctic Fox (2021.3.1) or newer
- JDK 11 or newer
- Android SDK 31 (Android 12) or newer
- Gradle 7.0.2 or newer

### Setup

1. Clone the repository
   ```
   git clone https://github.com/yourusername/kairix-todo-android.git
   ```

2. Open the project in Android Studio
   ```
   cd kairix-todo-android
   ./gradlew openIdea
   ```

3. Configure the API connection
   - Open `app/src/main/res/values/config.xml`
   - Update the `api_base_url` value to point to your Kairix Todo API instance
   - Obtain an API key from your Kairix Todo instance and add it to the app's settings

4. Build the project
   ```
   ./gradlew assembleDebug
   ```

5. Run the app
   ```
   ./gradlew installDebug
   ```

## Development

### Architecture

The app follows the MVVM (Model-View-ViewModel) architecture pattern with a clean architecture approach. See the [System Design](docs/system_design.md) document for detailed architecture information.

### Key Components

- **UI Layer**: Activities, Fragments, ViewModels
- **Domain Layer**: Use Cases, Domain Models
- **Data Layer**: Repositories, Data Sources
- **API Integration**: Retrofit, Moshi
- **Local Storage**: Room Database
- **Dependency Injection**: Dagger Hilt
- **Asynchronous Programming**: Kotlin Coroutines, Flow

### Testing

- Unit tests: `./gradlew testDebugUnitTest`
- Instrumented tests: `./gradlew connectedDebugAndroidTest`
- Code coverage report: `./gradlew createDebugCoverageReport`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Kairix Todo web service team
- Android Jetpack libraries
- Material Design components
