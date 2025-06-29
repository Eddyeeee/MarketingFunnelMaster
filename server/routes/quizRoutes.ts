import { Router } from 'express';
import { storage } from '../storage';

const router = Router();

// Quiz abrufen
router.get('/:quizId', async (req, res) => {
  try {
    const { quizId } = req.params;
    const quiz = await storage.getQuiz(quizId);
    
    if (quiz) {
      res.json({ success: true, quiz });
    } else {
      res.status(404).json({ success: false, message: 'Quiz nicht gefunden' });
    }
  } catch (error) {
    console.error('Quiz-Abruf Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

// Quiz-Antworten speichern
router.post('/:quizId/submit', async (req, res) => {
  try {
    const { quizId } = req.params;
    const { answers, leadData } = req.body;
    
    const result = await storage.submitQuizAnswers(quizId, answers, leadData);
    
    if (result) {
      res.json({ success: true, result });
    } else {
      res.status(500).json({ success: false, message: 'Quiz-Speicherung fehlgeschlagen' });
    }
  } catch (error) {
    console.error('Quiz-Speicherung Fehler:', error);
    res.status(500).json({ success: false, message: 'Interner Server-Fehler' });
  }
});

export default router; 