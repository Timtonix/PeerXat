# Spécifications techniques

## Chiffrement
- Avec la méthode TCP, on doit vérifier que chaque poste est bien autorisé à parler avec un autre.
  - Pour cela on peut utiliser le chiffrement RSA avec une clé GPG pour signer ses messages

## Ports
- Le port par défaut pour communiquer est le `50001`
- Quand on envoie un message, le port change tout le temps


## IP
- on doit faire en sorte de connaitre sa propre IP pour éviter de s'envoyer un ping à soi-même
- On utilise Netifaces car `socket.gethostbyname()` ne **marche pas** sur Linux