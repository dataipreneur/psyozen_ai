  import React from 'react'
  import VoiceAssistant from './components/com/VoiceAssistant'
import { ThemeProvider } from './components/ui/theme-provider'

  function App() {
    return (
  <>
 <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
 <VoiceAssistant/>
 </ThemeProvider>
  </>
    )
  }

  export default App