/*	HEADER
*  @Author:			Zachary Champion
*  Last Updated:	11 April 2016
*  Project:		
*  Shout Wall Log (for the programmer's personal use only)
*		This project will, at its most basic, record the number of shouts 
*			committed to the Shout Wall and the contents thereof as a record.
*		Other features to follow:
*			Shout Wall statistics
*				average shouts in the week
*				shouts to complete
*				average shouts to complete
*				Support of variable file names 
*					(by week start and end date for more ease of organization)
*				Warning when submitting too many "short" shouts in a row
*/

import java.util.*;
import java.io.*;
import java.text.*;

public class ShoutWall
{
	// Create the file and scanner handles.
	static Scanner Console;
	static PrintWriter outFile;
	static Scanner inFile;
				
	// This variable holds the constant output file name.
	static final String LogFile = "swlog.txt";
	
	public static void main(String[] args)
	{
		// Starts the program with the heading.
		programHeader();
		
		// Instantiate the handles.
		Console = new Scanner(System.in);
		
		while (true) {
			
			String Input = "";
			
			// Get a menu command from the user.
			System.out.print("Menu :: ");
			Input = Console.nextLine();
			
			// Decide what to do with the command.
			if (Input.startsWith("/")) {

				// Search the menu command tree.
				if (Input.toUpperCase().endsWith("DONE")) {
					
					// Exits the program.
					System.out.println("Exiting program.");
					System.exit(0);
				}
				else if (Input.toUpperCase().endsWith("LOG"))
				{
					System.out.println();
					Log();
				}
				else if (Input.toUpperCase().endsWith("SHOUTS"))
				{
					ShoutSummary();
					System.out.println();
				}
				else if (Input.toUpperCase().endsWith("TEST"))
				{
					try
					{
						outFile = new PrintWriter(new FileWriter(LogFile, true));
						
						String timeLog = new SimpleDateFormat("MM.dd").format(Calendar.getInstance().getTime());
						
						outFile.println("[SHOUT TEST " + timeLog + "]");
						
						System.out.println("Shout Wall Test entered in the Log.");
						System.out.println();
						
						outFile.close();
					}
					catch (Exception e)
					{
						e.printStackTrace();
					}
				}
				else if (Input.toUpperCase().startsWith("BUG", 1))
				{
					String BugInput;
					System.out.println();
					try
					{
						outFile = new PrintWriter(new FileWriter(LogFile, true));
						
						// Ask the user to enter a description of the bug.
						System.out.println("What's the bug? Tell me what's a-happenin': ");
						BugInput = Console.nextLine();
						System.out.println();
						
						// Enter the bug into the Shout Wall log.
						String timeLog = new SimpleDateFormat("MM.dd HH:mm").format(Calendar.getInstance().getTime());
						outFile.println("[BUG REPORT " + timeLog + "] \"" + BugInput + "\"");
						System.out.println("Bug entered in the Log:");
						System.out.println(BugInput);
						System.out.println();
						
						outFile.close();
					}
					catch (Exception e)
					{
						e.printStackTrace();
					}
				}
				else if (Input.toUpperCase().startsWith("FIN", 1))
				{
					System.out.println();
					finalizeLog();
				}
				else // If a wrong command is entered, display an error.
					System.out.println("Error: Command not recognized.");
			}
			else
			{	// If a command is not entered, display an error.
				System.out.println("Error: No command entered.");
				System.out.println("Please input a valid command.");
			}
		}
	}
	
	public static void ShoutSummary() {
		
		// Create a file reader handle.
		try {
			inFile = new Scanner(new FileReader(LogFile));
		}
		catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		// Create counter variables for the necessary things.
		int shouts = 0, tests = 0, bugs = 0;
		
		// Count how many shouts, tests, and bug reports are in the Log.
		System.out.println("Counting values...");
		while (inFile.hasNextLine())
		{
			String Line = inFile.nextLine();
		
			if (Line.toUpperCase().startsWith("LOG", 1))
				if (shouts < 250)
					shouts++;
			else if (Line.toUpperCase().startsWith("BUG", 1))	
				bugs++;
			else if (Line.toUpperCase().startsWith("SHOUT TEST", 1))
				tests++;
		}
		
		// Close the input file.
		inFile.close();
		
		// Calculate the amount due.
		double Amount = 0.00;
		System.out.println("Calculating...");
		if (shouts > 0)
			Amount += shouts * 0.20;
		if (tests > 0)
			Amount += tests * 5.00;
		if (bugs > 0)
			Amount += bugs * 2.00;
		
		// Output to the log and to the user the results of the count and computation.
		System.out.println();
		String SummaryString = "";
		
		if (shouts > 0)
			SummaryString += "Shouts Completed:  " + shouts + "\n";
		if (tests > 0)
			SummaryString += "Shout Wall Tests:  " + tests + "\n";
		if (bugs > 0)
			SummaryString += "Bugs Reported:     " + bugs + "\n";
			
		NumberFormat USD = NumberFormat.getCurrencyInstance();
		SummaryString += "Paypal Amount:     " + USD.format(Amount);
		
		System.out.println(SummaryString);
		System.out.println();		
	}

	public static void programHeader() {
		
		// Starts the program with a message to the user.
		System.out.println("Shout Wall Log");
		System.out.println();
	}
	
	public static void Log() {
		
		// logs the input to the Shout Wall Log.
		while (true) {
			String LogInput = "";
			
			// Get a menu command from the user.
			System.out.print("Log  :: ");
			LogInput = Console.nextLine();
			
			// Decide what to do with the input.
			if (LogInput.startsWith("/"))
			{
				// Search the menu command tree.
				if (LogInput.toUpperCase().endsWith("DONE"))
				{	// Exits the program.
					System.out.println("Exiting Log Entry.");
					System.out.println();
					break;
				}
				else if (LogInput.toUpperCase().startsWith("BUG", 1))
				{
					String BugInput;
					System.out.println();
					try
					{	outFile = new PrintWriter(LogFile);
						
						// Ask the user to enter a description of the bug.
						System.out.println("What's the bug? Tell me what's a-happenin':");
						BugInput = Console.nextLine();
						System.out.println();
						
						// Enter the bug into the Shout Wall log.
						String timeLog = new SimpleDateFormat("MM.dd HH:mm").format(Calendar.getInstance().getTime());
						
						outFile.println("[BUG REPORT " + timeLog + "] \"" + BugInput + "\"");
						
						System.out.println("Bug entered in the Log:");
						System.out.println(BugInput);
						System.out.println();
						
						outFile.close();
					}
					catch (Exception e)
					{
						e.printStackTrace();
					}
					finally
					{
						outFile.close();
					}
				}
				else if (LogInput.toUpperCase().endsWith("SHOUTS"))
				{
					int shouts = -1;
					
					try
					{
						// Create a file reader handle.
						inFile = new Scanner(new FileReader(LogFile));
					
						// Count how many shouts, tests, and bug reports are in the Log.
						System.out.println();
						while (inFile.hasNextLine())
						{
							String Line = inFile.nextLine();
							
							if (Line.toUpperCase().startsWith("LOG", 1))
								shouts++;
						}
						
						// Close the input file.
						inFile.close();
					}
					catch (Exception e) {
						e.printStackTrace();
					}
					
					if (shouts > 0)
						System.out.println("Shouts:  " + shouts);
					else 
						System.out.println("There aren't any shouts recorded yet! Get a move on!");
										
					System.out.println();
				}
				else // If a wrong command is entered, display an error.
					System.out.println("Error: Command not recognized.");
			}
			else
			{	// If a command is not entered, log the input string.
				try
				{
					outFile = new PrintWriter(new FileWriter(LogFile, true));
					
					String timeLog = new SimpleDateFormat("MM.dd HH:mm").format(Calendar.getInstance().getTime());
				
					outFile.println("[LOG  " + timeLog + "] \"" + LogInput + "\"");
					
					outFile.close();
				}
				catch (Exception e)
				{
					e.printStackTrace();
					continue;
				}
			}
		}
	}
	
	public static void finalizeLog()
	{		
		try
		{
			// Create a file reader handle.
			inFile = new Scanner(new FileReader(LogFile));
		
			// Create counter variables for the necessary things.
			int shouts = 0, tests = 0, bugs = 0;
		
			// Count how many shouts, tests, and bug reports are in the Log.
			System.out.println("Counting values...");
			while (inFile.hasNextLine())
			{
				String Line = inFile.nextLine();
			
				if (Line.toUpperCase().startsWith("LOG", 1))
					if (shouts < 250)
						shouts++;
				else if (Line.toUpperCase().startsWith("BUG", 1))	
					bugs++;
				else if (Line.toUpperCase().startsWith("SHOUT TEST", 1))
					tests++;
			}
		
			// Close the input file.
			inFile.close();
			
			// Calculate the amount due.
			double Amount = 0.00;
			System.out.println("Calculating...");
			if (shouts > 0)
				Amount += shouts * 0.20;
			if (tests > 0)
				Amount += tests * 5.00;
			if (bugs > 0)
				Amount += bugs * 2.00;
		
			// Output to the log and to the user the results of the count and computation.
			System.out.println();
			String InvoiceString = "[FINAL INVOICE]\n";
			InvoiceString += "Paypal Email:      Belgarion270@gmail.com\n";
			if (shouts > 0)
				InvoiceString += "Shouts Completed:  " + shouts + "\n";
			if (tests > 0)
				InvoiceString += "Shout Wall Tests:  " + tests + "\n";
			if (bugs > 0)
				InvoiceString += "Bugs Reported:     " + bugs + "\n";
				
			NumberFormat USD = NumberFormat.getCurrencyInstance();
			InvoiceString += "Paypal Amount:     " + USD.format(Amount);			

			try {
				
				outFile = new PrintWriter(new FileWriter(LogFile, true));
			
			} catch (IOException e) {
				// If an exception occurs, print the Stack trace (whatever that is) and exit.
				e.printStackTrace();
				System.exit(0);
			}
			
			System.out.println(InvoiceString);
			outFile.println(InvoiceString);
			
			outFile.close();
			
			System.out.println();
		}
		catch (Exception e)
		{
			System.out.println("Error finalizing Shout Wall Log.");
			e.printStackTrace();
			System.out.println();
		}
	}
}