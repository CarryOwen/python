#include "stdafx.h"
#include "mapfile.h"

CMapFile::CMapFile(char * pPath,bool bWrite,PVOID &pMap,DWORD &dwFileSize)
		:pImageView(pMap)
		,dwSize(dwFileSize)

{
	this->hFileHandle=INVALID_HANDLE_VALUE;
	this->hFileMapHandle=INVALID_HANDLE_VALUE;
	this->pImageView =NULL;
	this->dwSize =0;
	try
	{
		if(bWrite)
		{
			this->hFileHandle = CreateFileA(pPath, GENERIC_READ|GENERIC_WRITE,0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL , NULL);
		}
		else
		{
			this->hFileHandle = CreateFileA(pPath, GENERIC_READ,0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL , NULL);
		}
		if(this->hFileHandle==INVALID_HANDLE_VALUE)
		{
			throw (0);							
		}
		this->dwSize=GetFileSize(this->hFileHandle,NULL);
		if(this->dwSize==0)
		{
			throw (1);
		}
		if(bWrite)
		{
			this->hFileMapHandle=CreateFileMappingA(this->hFileHandle,NULL,PAGE_READWRITE,0,0,NULL);
		}
		else
		{
			this->hFileMapHandle=CreateFileMappingA(this->hFileHandle,NULL,PAGE_READONLY,0,0,NULL);
		}
		if(this->hFileMapHandle==INVALID_HANDLE_VALUE)
		{
			throw (2);
		}
		CloseHandle(this->hFileHandle);
		this->hFileHandle= INVALID_HANDLE_VALUE;
		if(bWrite)
		{
			this->pImageView=MapViewOfFile(this->hFileMapHandle,FILE_MAP_WRITE|FILE_MAP_READ,0,0,0);
		}
		else
		{
			this->pImageView=MapViewOfFile(this->hFileMapHandle,FILE_MAP_READ,0,0,0);
		}
		if(this->pImageView==NULL)
		{
			throw (4);
		}
	}
	catch(...)
	{
		this->pImageView=NULL;
	}

}

CMapFile::~CMapFile(void)
{
	try
	{
		if(this->pImageView!=NULL)
		{
			UnmapViewOfFile(this->pImageView);
		}
		if(this->hFileMapHandle!=INVALID_HANDLE_VALUE)
		{
			CloseHandle(this->hFileMapHandle);
		}
		if(this->hFileHandle!=INVALID_HANDLE_VALUE)
		{
			CloseHandle(this->hFileHandle);
		}
	}
	catch(...)
	{
	}
}


PIMAGE_SECTION_HEADER
__AddImportTable_GetEnclosingSectionHeader(
	DWORD rva,
	PIMAGE_NT_HEADERS pNTHeader
	)
{
	PIMAGE_SECTION_HEADER section = IMAGE_FIRST_SECTION(pNTHeader);
	unsigned i;

	for ( i=0; i < pNTHeader->FileHeader.NumberOfSections; i++, section++ )
		{
		// Is the RVA within this section?
		if ( (rva >= section->VirtualAddress) && 
			(rva < (section->VirtualAddress + section->Misc.VirtualSize)))
			return section;
		}

	return 0;
}


int
AddImportDll(
			 IN HANDLE hFile,
			 IN LPSTR  lpDllName,
			 IN DWORD  dwBase,
			 IN PIMAGE_NT_HEADERS pNTHeader
			 )
{
	//
	// ????OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress
	// ????????????RVA, ??????RVA????ImportTable??????Section,????????Offset,????:
	//    Offset = (INT)(pSection->VirtualAddress - ->PointerToRawData)
	// ????????Offset????????????ImportTable??????.pSection
	//
	PIMAGE_IMPORT_DESCRIPTOR  pImportDesc = 0;
	PIMAGE_SECTION_HEADER    pSection = 0;
	PIMAGE_THUNK_DATA      pThunk, pThunkIAT = 0;
	int Offset = -1;

	pSection = __AddImportTable_GetEnclosingSectionHeader(
		pNTHeader->OptionalHeader.DataDirectory
		[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress,
		pNTHeader);
	if(!pSection)
		{
		fprintf(stderr, "??????????????????..\n");
		return -1;
		}

	Offset = (int) (pSection->VirtualAddress - pSection->PointerToRawData);

	//
	// ????ImportTable??????????????
	//
	pImportDesc =(PIMAGE_IMPORT_DESCRIPTOR)(pNTHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress - Offset + dwBase);

	// ??????????DLL?????? ,??????????????	---2012-11-20
	//int nImportDllCount = 0;
	//while(1)
	//{
	//	if ((pImportDesc->TimeDateStamp==0 ) && (pImportDesc->Name==0))
	//		break;
	//	pThunk   = (PIMAGE_THUNK_DATA)(pImportDesc->Characteristics);
	//	pThunkIAT = (PIMAGE_THUNK_DATA)(pImportDesc->FirstThunk);
	//	if(pThunk == 0 && pThunkIAT == 0)
	//		return -1;
	//	nImportDllCount++;
	//	pImportDesc++;
	//}
	////
	//// ????pImportDesc????,??????????????????????????????.
	////
	//pImportDesc -= nImportDllCount;
	// ??????????DLL?????? ,??????????????---2012-11-20

	int nImportDllCount = 5;//??????????????DLL??????5??

	//
	// ????ImportTable????Section??RawData??????????????????,????????:
	//    dwOrigEndOfRawDataAddr = pSection->PointerToRawData + pSection->Misc.VirtualSize
	//
	DWORD dwEndOfRawDataAddr = pSection->PointerToRawData + pSection->Misc.VirtualSize;
	PIMAGE_IMPORT_DESCRIPTOR pImportDescVector = 
		(PIMAGE_IMPORT_DESCRIPTOR)HeapAlloc(GetProcessHeap(), HEAP_ZERO_MEMORY, 20 * (nImportDllCount+1));
	if(pImportDescVector == NULL)
		{
		//fprintf(stderr, "????????????. --??????: %d\n", GetLastError());
		return -1;
		}
	CopyMemory(pImportDescVector+1, pImportDesc, 20*nImportDllCount);


	//
	// ??????????????????
	//
	struct _Add_Data
		{
		char      szDllName[MAX_PATH];                // ????DLL??????
		int           nDllNameLen;                // ????????????????????
		WORD      Hint;                           // ??????????Hint
		char   szFuncName[MAX_PATH];           // ??????????????
		int    nFuncNameLen;                // ??????????????????????
		int    nTotal;                           // ????????????
		} Add_Data;
	memset(Add_Data.szDllName,0,MAX_PATH);
	memset(Add_Data.szFuncName,0,MAX_PATH);
	strcpy(Add_Data.szDllName, lpDllName);
	strcpy(Add_Data.szFuncName, "CBFunA");

	//
	// +1????&#39;\0&#39;????
	//
	Add_Data.nDllNameLen  = strlen(Add_Data.szDllName) + 1;
	Add_Data.nFuncNameLen = strlen(Add_Data.szFuncName) + 1;
	Add_Data.Hint = 0;
	//
	// ??????????????????
	//
	Add_Data.nTotal = Add_Data.nDllNameLen + sizeof(WORD) + Add_Data.nFuncNameLen;

	//
	// ????ImportTable??????Section????????????????????????????ImportTable.
	// ????????RawData??????????????????pSection->VirtualSize??,??????????????ImportTable??????
	// ??????????????.
	//
	// nTotalLen ????????????????????
	// Add_Data.nTotal ????????DLL????,Hint????????????????????????.
	// 8 ??IMAGE_IMPORT_BY_NAME??????????.
	// 20*(nImportDllCount+1) ??????ImportTable??????.
	//
	int nTotalLen = Add_Data.nTotal + 8 + 20*(nImportDllCount+1);
	//      printf("TotalLen: %d byte(s)\n", nTotalLen);
	if(pSection->Misc.VirtualSize + nTotalLen > pSection->SizeOfRawData)
		{
		return -1;
		}

	IMAGE_IMPORT_DESCRIPTOR Add_ImportDesc;
	//
	// ThunkData??????????
	//
	Add_ImportDesc.Characteristics = dwEndOfRawDataAddr + Add_Data.nTotal + Offset;
	Add_ImportDesc.TimeDateStamp = -1;
	Add_ImportDesc.ForwarderChain = -1;
	//
	// DLL??????RVA
	//
	Add_ImportDesc.Name = dwEndOfRawDataAddr + Offset;
	Add_ImportDesc.FirstThunk = Add_ImportDesc.Characteristics;

	CopyMemory(pImportDescVector, &Add_ImportDesc, 20);

	//
	// ??????????????
	//
	DWORD dwBytesWritten = 0;
	DWORD dwBuffer = dwEndOfRawDataAddr + Offset + Add_Data.nTotal + 8;
	long  lDistanceToMove = (long)&(pNTHeader->OptionalHeader.DataDirectory
		[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress) - dwBase;
	int nRet =0;

	//
	// ????IMAGE_DIRECTOR_ENTRY_IMPORT??VirtualAddress??????,
	// ????????????????????????
	//
	SetFilePointer(hFile, lDistanceToMove, NULL, FILE_BEGIN);

	//      printf("OrigEntryImport: %x\n", pNTHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress);
	nRet = WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	if(!nRet)
		{
		//fprintf(stderr, "?? ????????????????????????. --??????: %d\n", GetLastError());
		return -1;
		}
	//      printf("NewEntryImport: %x\n", pNTHeader->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress);
	//
	// ??????????????
	//
	dwBuffer = pNTHeader->OptionalHeader.DataDirectory
		[IMAGE_DIRECTORY_ENTRY_IMPORT].Size + 40;
	nRet = WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	if(!nRet)
		{
		//fprintf(stderr, "?? ??????????????????????????. --??????: %d\n", GetLastError());
		return -1;
		}

	//
	// ????[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT]??VirtualAddress??Size????,??????0
	//
	lDistanceToMove = (long)&(pNTHeader->OptionalHeader.DataDirectory
		[IMAGE_DIRECTORY_ENTRY_BOUND_IMPORT].VirtualAddress) - dwBase;
	dwBuffer = 0;
	SetFilePointer(hFile, lDistanceToMove, NULL, FILE_BEGIN);
	WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);

	//
	// ????ImportTable????????????
	//
	lDistanceToMove = (long)&(pSection->Misc.VirtualSize) - dwBase;
	SetFilePointer(hFile, lDistanceToMove, NULL, FILE_BEGIN);
	dwBuffer = pSection->Misc.VirtualSize + nTotalLen;
	nRet = WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	if(!nRet)
		{
		//fprintf(stderr, "????????????????????????????. --??????: %d\n", GetLastError());
		return -1;
		}
	//
	// ????SECTION??Characteristics??????????E0000020
	//
	lDistanceToMove = (long)&(pSection->Characteristics) - dwBase;
	dwBuffer = 0xE0000020;
	SetFilePointer(hFile, lDistanceToMove, NULL, FILE_BEGIN);
	nRet = WriteFile(hFile, (PVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	if(!nRet)
		{
		//fprintf(stderr, "??E0000020??????????????. --??????: %d\n", GetLastError());
		return -1;
		}

	//
	// ??????????????????DLL????
	//
	lDistanceToMove = dwEndOfRawDataAddr;
	SetFilePointer(hFile, lDistanceToMove, NULL, FILE_BEGIN);
	nRet = WriteFile(hFile, Add_Data.szDllName, Add_Data.nDllNameLen, &dwBytesWritten, NULL);
	nRet = WriteFile(hFile, (LPVOID)&(Add_Data.Hint), sizeof(WORD), &dwBytesWritten, NULL);
	nRet = WriteFile(hFile, Add_Data.szFuncName, Add_Data.nFuncNameLen, &dwBytesWritten, NULL);
	dwBuffer = dwEndOfRawDataAddr + Add_Data.nDllNameLen + Offset;
	nRet = WriteFile(hFile, (LPVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	dwBuffer = 0;
	nRet = WriteFile(hFile, (LPVOID)&dwBuffer, 4, &dwBytesWritten, NULL);
	nRet = WriteFile(hFile, (LPVOID)pImportDescVector, 20*(nImportDllCount+1), &dwBytesWritten, NULL);
	HeapFree(GetProcessHeap(), 0, pImportDescVector);

	return 0;
} 



LPVOID HookIMEdllIAT(char *SouceMode,char* hookdll)
{
	DWORD dwFileSize =0 ;
	LPVOID pPeImage=NULL;
	CMapFile cMapFile(SouceMode,true,pPeImage,dwFileSize);
	if(pPeImage!=NULL)
		{
			BYTE *pFileImage = (BYTE*)pPeImage;
			PIMAGE_DOS_HEADER pDosHeader = (PIMAGE_DOS_HEADER)pFileImage;
			PIMAGE_FILE_HEADER pFileHeader =(PIMAGE_FILE_HEADER)(pFileImage+pDosHeader->e_lfanew+4);
			PIMAGE_OPTIONAL_HEADER32 pOptionalHeader =(PIMAGE_OPTIONAL_HEADER32)(pFileImage+pDosHeader->e_lfanew+4+sizeof(IMAGE_FILE_HEADER));
			PIMAGE_NT_HEADERS  pNTHeader=(PIMAGE_NT_HEADERS)&((const unsigned char *)(pFileImage))[pDosHeader->e_lfanew];

			//??????????????????????????????????????????????????????????????????????
			HANDLE handle = CreateFileA(SouceMode,GENERIC_READ|GENERIC_WRITE,FILE_SHARE_READ|FILE_SHARE_WRITE,NULL,OPEN_EXISTING,FILE_ATTRIBUTE_NORMAL,0);

			AddImportDll(handle,hookdll,(DWORD)pFileImage,pNTHeader);

			CloseHandle(handle);

		} 

	return pPeImage;
}
