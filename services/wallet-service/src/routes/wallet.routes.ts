import { Router } from 'express';
import { WalletController } from '../controllers/wallet.controller';
import { authenticate } from '../middleware/auth.middleware';

const router = Router();
const walletController = new WalletController();

router.use(authenticate);

router.get('/', (req, res) => walletController.getWallet(req, res));
router.get('/transactions', (req, res) => walletController.getTransactions(req, res));
router.post('/deposit', (req, res) => walletController.deposit(req, res));
router.post('/withdraw', (req, res) => walletController.withdraw(req, res));

export default router;
