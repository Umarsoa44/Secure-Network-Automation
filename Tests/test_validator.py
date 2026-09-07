import unittest
import sys
from pathlib import Path

# Add Scripts directory to path to import main functions
sys.path.append(str(Path(__file__).resolve().parent.parent / "Scripts"))
from main import evaluate_config

class TestNetworkSecurityValidator(unittest.TestCase):
    
    def setUp(self):
        self.policy = {
            "ssh_version": 2,
            "telnet_allowed": False,
            "http_management_allowed": False,
            "password_encryption_required": True,
            "unused_interfaces_should_be_disabled": True
        }

    def test_compliant_configuration(self):
        secure_config = """
        hostname SECURE-RTR
        ip ssh version 2
        service password-encryption
        no ip http server
        """
        score, findings = evaluate_config(secure_config, self.policy)
        self.assertEqual(score, 100)
        self.assertEqual(len(findings), 0)

    def test_insecure_configuration(self):
        insecure_config = """
        hostname INSECURE-SW
        ip http server
        line vty 0 4
         transport input telnet ssh
        """
        score, findings = evaluate_config(insecure_config, self.policy)
        self.assertLess(score, 100)
        self.assertTrue(any("Telnet" in f for f in findings))
        self.assertTrue(any("HTTP" in f for f in findings))

if __name__ == "__main__":
    unittest.main()