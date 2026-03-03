// --------------------------------------------------------------------------------------------------------
// Lernkarten AP2 - Quiz Anwendung (C#)
// Quiz-System für AP2 Lernkarten mit Counter-Verwaltung
// Fragedaten: AP2lernkarten.json (ohne Counter - nur Frage + Antworten)
// Counter-Daten: AP2lernkarten_counter.json (getrennt, nicht in Git!)
// Aufruf von Python/PyQt6 GUI möglich
//
// woher kommt das : dies ist eine übersetzug des orginal quizes das in python geschrieben wurde. 
//                    übersetzt durch ki um den unterscheid zu sehen da es schon mal da war wurde es (keine 1 zu 1 übersetzung eigenheiten der sprachen erforderten änderungen)
//                    hier zu einer weiter fortgeschritten übung gemacht selbst umwandeln der datei um sie nutzen zu können 
//                    beachte das die gui dir den weg zueigt wie du die datei nutzbar machen kasnst
// --------------------------------------------------------------------------------------------------------

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Text.Json.Serialization;

// ===== MODELLE =====
public class QuizFrage
{
    [JsonPropertyName("Id")]
    public int Id { get; set; }

    [JsonPropertyName("Frage")]
    public string Frage { get; set; }

    [JsonPropertyName("Antwort1")]
    public string Antwort1 { get; set; }

    [JsonPropertyName("Antwort2")]
    public string Antwort2 { get; set; }

    [JsonPropertyName("KorrekteAntwortIndex")]
    public int KorrekteAntwortIndex { get; set; } // 1 oder 2
}

public class QuizCounter
{
    [JsonPropertyName("Id")]
    public int Id { get; set; }

    [JsonPropertyName("AntwortCounter")]
    public int AntwortCounter { get; set; }
}

// ===== HAUPT-PROGRAMM =====
class Program
{
    static string fragenPfad = "AP2lernkarten.json";
    static string counterPfad = "AP2lernkarten_counter.json";

    static void Main(string[] args)
    {
        // Optionale Command-Line Argumente: --help, --setup, oder interaktiv
        if (args.Length > 0 && args[0] == "--help")
        {
            ZeigeHilfe();
            return;
        }

        if (args.Length > 0 && args[0] == "--setup")
        {
            InitialisiereCounterJSON();
            Console.WriteLine("Counter-JSON wurde initialisiert.");
            return;
        }

        // Normal-Modus: Eine Frage stellen
        StartQuiz();
    }

    static void StartQuiz()
    {
        try
        {
            // 1. Laden
            var alleFragen = LadeFragen();
            var alleCounter = LadeCounter();

            if (alleFragen.Count == 0)
            {
                Console.WriteLine("Fehler: Keine Fragen in AP2lernkarten.json gefunden.");
                return;
            }

            // 2. Beste Frage wählen (mit höchstem Counter)
            var aktuelleFrage = WahleBesteFrage(alleFragen, alleCounter);

            // 3. Zeige Frage
            ZeigeFrage(aktuelleFrage);

            // 4. Eingabe
            Console.Write("\nDeine Antwort (1 oder 2): ");
            string eingabe = Console.ReadLine();

            // 5. Verarbeite Antwort
            if (int.TryParse(eingabe, out int gewaehlt))
            {
                var counter = alleCounter.FirstOrDefault(c => c.Id == aktuelleFrage.Id);
                if (counter == null)
                {
                    counter = new QuizCounter { Id = aktuelleFrage.Id, AntwortCounter = 0 };
                    alleCounter.Add(counter);
                }

                if (gewaehlt == aktuelleFrage.KorrekteAntwortIndex)
                {
                    Console.WriteLine("\n✓ Richtig!");
                    counter.AntwortCounter = Math.Max(0, counter.AntwortCounter - 1);
                }
                else
                {
                    var korrekt = aktuelleFrage.KorrekteAntwortIndex == 1 
                        ? aktuelleFrage.Antwort1 
                        : aktuelleFrage.Antwort2;
                    Console.WriteLine($"\n✗ Falsch! Die richtige Antwort ist: {korrekt}");
                    counter.AntwortCounter++;
                }

                SpeichereCounter(alleCounter);
            }
            else
            {
                Console.WriteLine("Ungültige Eingabe.");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Fehler: {ex.Message}");
        }
    }

    static QuizFrage WahleBesteFrage(List<QuizFrage> fragen, List<QuizCounter> counter)
    {
        // Sortiere nach Counter (absteigend) - höchste Counter zuerst
        var fragenMitCounter = fragen.Select(f => new
        {
            Frage = f,
            Counter = counter.FirstOrDefault(c => c.Id == f.Id)?.AntwortCounter ?? 0
        }).OrderByDescending(x => x.Counter).First();

        return fragenMitCounter.Frage;
    }

    static void ZeigeFrage(QuizFrage frage)
    {
        Console.WriteLine($"\n{'=' * 60}");
        Console.WriteLine($"FRAGE {frage.Id}: {frage.Frage}");
        Console.WriteLine($"{'=' * 60}");
        Console.WriteLine($"1) {frage.Antwort1}");
        Console.WriteLine($"2) {frage.Antwort2}");
    }

    static List<QuizFrage> LadeFragen()
    {
        if (!File.Exists(fragenPfad))
            throw new FileNotFoundException($"Datei nicht gefunden: {fragenPfad}");

        string json = File.ReadAllText(fragenPfad);
        return JsonSerializer.Deserialize<List<QuizFrage>>(json) ?? new();
    }

    static List<QuizCounter> LadeCounter()
    {
        if (!File.Exists(counterPfad))
            return new(); // Leer, wenn Datei nicht existiert

        string json = File.ReadAllText(counterPfad);
        return JsonSerializer.Deserialize<List<QuizCounter>>(json) ?? new();
    }

    static void SpeichereCounter(List<QuizCounter> counter)
    {
        var options = new JsonSerializerOptions { WriteIndented = true };
        string json = JsonSerializer.Serialize(counter, options);
        File.WriteAllText(counterPfad, json);
    }

    static void InitialisiereCounterJSON()
    {
        var fragen = LadeFragen();
        var counter = fragen.Select(f => new QuizCounter 
        { 
            Id = f.Id, 
            AntwortCounter = 5 
        }).ToList();

        SpeichereCounter(counter);
    }

    static void ZeigeHilfe()
    {
        Console.WriteLine("AP2 Lernkarten Quiz");
        Console.WriteLine("Nutzung:");
        Console.WriteLine("  main.exe                 - Startet Quiz mit einer Frage");
        Console.WriteLine("  main.exe --setup         - Initialisiert Counter-JSON");
        Console.WriteLine("  main.exe --help          - Zeigt diese Hilfe");
    }
}


