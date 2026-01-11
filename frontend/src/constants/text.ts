export const UI_TEXT = {
  titles: {
    roleSelection: 'Who is fixing this?',
    roleSubtitle: 'Select your expert persona to tune the AI model.',
    back: 'Change Role',
    plan: 'Resolution Plan',
    warnings: 'Heads up!',
  },
  roles: {
    dev: {
      title: 'Developer',
      desc: 'Focus on code logic, exceptions & libraries.',
      labels: {
        description: 'Describe the Bug',
        descHint: 'e.g. NullReferenceException in module Auth',
        logs: 'Stack Trace',
        logsHint: 'Paste compiler or runtime errors...',
        context: 'Tech Stack',
        contextHint: 'Language, Libraries, Framework versions...',
      },
    },
    devops: {
      title: 'DevOps / SRE',
      desc: 'Focus on infrastructure, network & clusters.',
      labels: {
        description: 'Incident Summary',
        descHint: 'e.g. High Latency on API Gateway',
        logs: 'System Logs',
        logsHint: 'Access logs, Syslogs, K8s events...',
        context: 'Infrastructure',
        contextHint: 'AWS, Kubernetes, DB Topology...',
      },
    },
  },
  actions: {
    generate: 'Generate Fix Plan',
    analyzing: 'Analyzing patterns...',
    copy: 'Copy to Clipboard',
  },
};
