

#if 0
class HookData {
	public:
		HookData(std::string python_name, std::string python_header);
		set_hook(LPVOID adr, VoidFunc hook);
		VoidFunc *m_trampolin;
		/* See http://civ4bug.sourceforge.net/PythonAPI/ */
		std::string m_python_name;
		std::string m_python_header;

	private:
		LPVOID m_adr;
		VoidFunc *m_hook;
};
#endif
/*
HookData::SetHook(LPVOID adr, VoidFunc *hook){
	m_hook = hook;
	m_adr = adr;
	MH_CreateHook(m_adr, m_hook,
			reinterpret_cast<void**>((LPVOID)&m_trampolin) );
}*/

	/*
void init_rescacer_hooks(){
		 HookData *setText = new HookData("setText",
		 "STRING szName, STRING szAtttachTo, STRING szText, INT uiFlags,"
		 " FLOAT fX, FLOAT fY, FLOAT fZ, FontType eFont,"
		 " WidgetType eType, INT iData1, INT iData2)"
		 );
		 std::function<VoidFunc> _func = [](int i) {
		 FFMUL(0x30, Factor);
		 FFMUL(0x34, Factor);
		 setText->m_trampolin();
		 };
		 setText->set_hook((LPVOID)0x00570E70, _func);

		 data.push_back(setText);
}
		 */


