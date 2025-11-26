import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration du test de charge
export const options = {
  stages: [
    { duration: '30s', target: 20 }, // Warm up: monter à 20 users en 30s
    { duration: '2m', target: 100 }, // Load: monter à 100 users (grosse charge pour HPA)
    { duration: '1m', target: 0 },   // Cool down: redescendre à 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% des requêtes doivent être < 500ms
  },
};

export default function () {
  // On tape sur le service interne du cluster (DNS Kubernetes)
  const res = http.get('http://back-cluster-ip-service:4000/');
  
  // Vérifications
  check(res, {
    'status was 200': (r) => r.status == 200,
    'transaction time OK': (r) => r.timings.duration < 500,
  });

  // Pause aléatoire entre 0.1s et 1s pour simuler un comportement humain (ou pas)
  sleep(1);
}
