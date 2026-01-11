export interface RoleDefinition {
    id: string;
    title: string;
    subtitle: string;
    icon: string;
    color: string;
    bgClass: string;
    darkClass: string;
    inputs: {
        description: string;
        descHint: string;
        logs: string;
        logsHint: string;
        context: string;
        contextHint: string;
    };
}

export const ROLES: Record<string, RoleDefinition> = {
    dev: {
        id: 'dev',
        title: 'Developer',
        subtitle: 'Focus on code logic, exceptions & libraries.',
        icon: 'code',
        color: 'accent',
        bgClass: 'bg-deep-purple-1',
        darkClass: 'bg-deep-purple-10',
        inputs: {
            description: 'Describe the Bug',
            descHint: 'e.g. NullReferenceException in module Auth',
            logs: 'Stack Trace',
            logsHint: 'Paste compiler or runtime errors...',
            context: 'Tech Stack',
            contextHint: 'Language, Libraries, Framework versions...',
        },
    },
    devops: {
        id: 'devops',
        title: 'DevOps / SRE',
        subtitle: 'Focus on infrastructure, network & clusters.',
        icon: 'dns',
        color: 'secondary',
        bgClass: 'bg-cyan-1',
        darkClass: 'bg-cyan-9',
        inputs: {
            description: 'Incident Summary',
            descHint: 'e.g. High Latency on API Gateway',
            logs: 'System Logs',
            logsHint: 'Access logs, Syslogs, K8s events...',
            context: 'Infrastructure',
            contextHint: 'AWS, Kubernetes, DB Topology...',
        },
    },
};

export const getRolesList = () => Object.values(ROLES);

export const getRoleConfig = (id: string | null): RoleDefinition => {
    if (id && ROLES[id]) {
        return ROLES[id];
    }
    return ROLES['dev']!;
};
