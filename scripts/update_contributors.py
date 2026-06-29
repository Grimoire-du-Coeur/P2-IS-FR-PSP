import json
import urllib.request
import os
import time
import sys

REPO = "chenetulipe/P2-FR-IS-PSP"
API_URL = f"https://api.github.com/repos/{REPO}/stats/contributors"
TOKEN = os.environ.get("GITHUB_TOKEN")

def fetch_stats(retries=15):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if TOKEN:
        headers['Authorization'] = f"Bearer {TOKEN}"
        
    req = urllib.request.Request(API_URL, headers=headers)
    
    for i in range(retries):
        try:
            with urllib.request.urlopen(req) as response:
                if response.status == 202:
                    print(f"[{i+1}/{retries}] GitHub génère les statistiques en arrière-plan, attente de 5 secondes...")
                    time.sleep(5)
                    continue
                data = json.loads(response.read().decode('utf-8'))
                return data
        except Exception as e:
            print(f"Erreur lors de la récupération des stats: {e}")
            time.sleep(5)
    return None

def main():
    print("Début du script de récupération des statistiques...")
    data = fetch_stats()
    if not data:
        print("Erreur : Impossible de récupérer les statistiques GitHub après plusieurs tentatives.")
        sys.exit(1)

    print("Statistiques récupérées avec succès. Traitement en cours...")

    # Trier par total de commits décroissant (assure que le 1er a le plus de commits)
    data.sort(key=lambda x: x['total'], reverse=True)

    stats_md = "### Statistiques Globales du Code\n\n"
    stats_md += "| Contributeur | 💾 Commits | ➕ Lignes Ajoutées | ➖ Lignes Supprimées |\n"
    stats_md += "|:---|:---:|:---:|:---:|\n"

    top_10_commits = data[:10]
    
    # Trier pour les Top 10 Ajouts
    data_additions = sorted(data, key=lambda x: sum(w['a'] for w in x['weeks']), reverse=True)[:10]
    
    # Trier pour les Top 10 Suppressions
    data_deletions = sorted(data, key=lambda x: sum(w['d'] for w in x['weeks']), reverse=True)[:10]

    for contributor in data:
        author = contributor['author']['login']
        total_commits = contributor['total']
        total_a = sum(week['a'] for week in contributor['weeks'])
        total_d = sum(week['d'] for week in contributor['weeks'])
        stats_md += f"| **@{author}** | {total_commits} | +{total_a} | -{total_d} |\n"

    graphs_md = "### Répartition des Contributions (Top 10)\n\n"
    
    # Graphique Commits
    graphs_md += "#### Volume de Commits\n```mermaid\npie title Top 10 - Commits\n"
    for c in top_10_commits:
        graphs_md += f'    "{c["author"]["login"]}" : {c["total"]}\n'
    graphs_md += "```\n\n"

    # Graphique Ajouts
    graphs_md += "#### Lignes Ajoutées\n```mermaid\npie title Top 10 - Lignes Ajoutées\n"
    for c in data_additions:
        total_a = sum(w['a'] for w in c['weeks'])
        if total_a > 0:
            graphs_md += f'    "{c["author"]["login"]}" : {total_a}\n'
    graphs_md += "```\n\n"

    # Graphique Suppressions
    graphs_md += "#### Lignes Supprimées\n```mermaid\npie title Top 10 - Lignes Supprimées\n"
    for c in data_deletions:
        total_d = sum(w['d'] for w in c['weeks'])
        if total_d > 0:
            graphs_md += f'    "{c["author"]["login"]}" : {total_d}\n'
    graphs_md += "```\n"

    final_content = stats_md + "\n" + graphs_md

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, "..", "CREDITS.md")
    
    if not os.path.exists(filepath):
        print(f"Erreur: Le fichier {filepath} n'existe pas.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = "<!-- STATS_START -->"
    end_marker = "<!-- STATS_END -->"

    if start_marker in content and end_marker in content:
        before = content.split(start_marker)[0]
        after = content.split(end_marker)[1]
        new_content = before + start_marker + "\n\n" + final_content + "\n" + end_marker + after
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("CREDITS.md mis à jour avec succès !")
    else:
        print("Erreur: Les balises <!-- STATS_START --> et <!-- STATS_END --> sont introuvables dans CREDITS.md.")
        sys.exit(1)

if __name__ == "__main__":
    main()
